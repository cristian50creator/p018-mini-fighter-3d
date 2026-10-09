from math import sin, cos, tau
from ursina import Entity, Mesh, Vec3, color, distance


class CheckpointCourse:
    """Túnel ligero con estructura alámbrica que sigue la ruta del punto de control para el avión caza."""

    def __init__(self):
        self.positions = [
            Vec3(0, 3, 18), Vec3(5, 4, 38), Vec3(10, 6, 59),
            Vec3(4, 8, 81), Vec3(-5, 7, 103), Vec3(-9, 5, 126),
            Vec3(-3, 4, 149), Vec3(0, 3, 173),
        ]
        self.current = 0
        self.radius = 3.5
        self.rings = []
        self._build_tunnel()
        self._refresh_colors()

    def _ring_points(self, center, radius, segments=32):
        # El recorrido avanza a lo largo del eje +Z, por lo que cada anillo esta en el plano XY.
        return [center + Vec3(cos(tau * i / segments) * radius,
                              sin(tau * i / segments) * radius, 0)
                for i in range(segments)]

    def _line(self, points, tint, thickness=2):
        '''
        return Entity(model=Mesh(vertices=points, mode='line', thickness=thickness),
                              color=tint, double_sided=True)
        '''
        mesh = Mesh(
            vertices=points,
            #colors=[tint] * len(points),
            mode='line',
            thickness=thickness
        )

        return Entity(
            model=mesh,
            color=tint,
            double_sided=True,
            unlit=True
        )
        

    def _build_tunnel(self):
        # Estructura alámbrica abierta de aspecto translúcido; sin paredes sólidas ni colisiones.
        # Actualizacion del color, para que se vea mejor, algo gris.
        tunnel_ring_color = color.rgb(125, 135, 145)
        tunnel_line_color = color.rgb(90, 100, 110)
        checkpoint_color = color.azure

        centers = [Vec3(0, 3, 0)] + self.positions

        self.rings = []
        self.glow_rings = []

        for center in centers:
            ring_points = self._ring_points(center, self.radius)
            self._line(ring_points + [ring_points[0]], tunnel_ring_color, 1)
        for i in range(12):
            angle = tau * i / 12
            offset = Vec3(cos(angle) * self.radius, sin(angle) * self.radius, 0)
            self._line([p + offset for p in centers], tunnel_line_color, 1)

        for position in self.positions:
            points = self._ring_points(position, self.radius)

            main_ring = self._line(
                points + [points[0]],
                color.azure,
                5
            )

            glow_points = self._ring_points(
                position,
                self.radius * 1.06
            )

            glow_ring = self._line(
                glow_points + [glow_points[0]],
                color.rgb(45, 110, 200),
                9
            )

            self.rings.append(main_ring)
            self.glow_rings.append(glow_ring)

    @property
    def total(self):
        return len(self.positions)

    @property
    def finished(self):
        return self.current >= self.total

    def _refresh_colors(self):
        for i, ring in enumerate(self.rings):
            is_active = i == self.current
            is_pending = i >= self.current

            ring.color = (
                color.rgb(180,255,0)
                if is_active
                else color.azure
            )

            ring.visible = is_pending

            glow_rings = self.glow_rings[i]

            glow_rings.color = (
                color.rgb(120,210,0)
                if is_active
                else color.rgb(45,110,200)
            )

            glow_rings.visible = is_pending


            #ring.color = color.lime if i == self.current else color.azure
            #ring.visible = i >= self.current
            

    def check(self, aircraft):
        if self.finished:
            return False
        target = self.positions[self.current]
        # Se cruza un punto de control cuando el avión atraviesa esa sección de plano.
        if aircraft.z >= target.z and distance(Vec3(aircraft.x, aircraft.y, 0),
                                               Vec3(target.x, target.y, 0)) <= self.radius:
            self.current += 1
            self._refresh_colors()
            return True
        return False

    def reset(self):
        self.current = 0
        self._refresh_colors()
