---
title: Wrapper FCF
client: Sinoficina (producto propio)
status: draft # draft | final
created: 2026-10-22
updated: 2026-10-22
---

# PRD: Wrapper FCF

## 0. Propósito del documento

Este PRD define qué construimos en la v1 de Wrapper FCF. Lo leen Luis (dueño del producto), el equipo de Sinoficina y los agentes que implementarán cada parte. Se basa en la entrevista de producto del 22/10/2026 (registrada en `.decision-log.md`), en el dossier "Guinardó: rivales Grup 20" hecho a mano por Luis (`materials/guinardo-dossier.html`) y en la ingeniería inversa de la API interna de fcf.cat (`fcf/ENDPOINTS.md`). Cada feature de §5 se convertirá en una spec de implementación con `nch-spec`. El PRD describe capacidades, no tecnología.

## 1. Visión

Wrapper FCF es la forma cómoda de seguir a un **Equipo** de la Federació Catalana de Futbol. La web oficial (fcf.cat) tiene todos los datos, pero cuesta encontrarlos, no se adapta al móvil y no saca conclusiones. Wrapper FCF coge esos mismos datos públicos y los presenta como una app de resultados moderna, al estilo de Sofascore: buscas tu Equipo, lo sigues, y desde ese momento tienes su calendario, resultados, clasificación, Actas, plantilla y estadísticas, con los colores de tu Equipo.

Encima de eso, la app hace lo que hoy Luis hace a mano cada semana: preparar al rival. Un **Gestor** pide el **Dossier** del próximo rival y en minutos tiene su forma, cómo marca y encaja por **Tramos**, su once más repetido, su plantilla y sus sanciones. El Dossier solo lo ve quien gestiona, para que no llegue al rival.

La app nace para el Guinardó C.F., pero cualquier Equipo de la FCF puede usarla desde el primer día sin alta manual. Está preparada para que, en el futuro, un Gestor pague por desbloquear funciones para su Equipo o Club.

## 2. Contexto del encargo

- **Producto propio de Sinoficina**, sin cliente externo. Luis decide el producto. Las únicas incógnitas externas (permiso de la FCF, datos de menores) viven en `client-questions.md`.
- **Tipo de proyecto:** MVP de validación con el propio club (Guinardó C.F.), construido para abrirse a cualquier club de la FCF sin rehacerlo.
- **Entrega en dos hitos** (ver §7):
  - **Hito 1, "el Guinardó la usa":** seguimiento, estadísticas y tema automático, sin cuentas.
  - **Hito 2, "listo para otros clubs":** cuentas, roles, Dossier, notificaciones y marca manual.
- **Urgencia:** Luis quiere una primera versión del Hito 1 online para el Guinardó A el 23/10/2026, antes del partido Darna 2019 – Guinardó (sábado 24/10, 20:15). Se cierra primero este PRD y después se hace la spec de esa primera entrega.
- **Datos:** dependemos al 100 % de la API interna, pública y no documentada de fcf.cat. Puede cambiar sin aviso.
- **Presupuesto:** planes gratuitos de la infraestructura elegida.
- **Restricciones técnicas** (decididas por Luis, se aplican en las specs, no en este PRD): React + Supabase + Vercel, formato PWA.

## 3. Usuarios

### 3.1 Roles

- **Seguidor**: cualquier persona que sigue uno o varios Equipos: jugadores, cuerpo técnico, familias, aficionados. No necesita Cuenta. Quiere saber cuándo se juega y cómo ha ido.
- **Gestor**: persona con Cuenta a quien el Administrador ha aprobado una Solicitud de gestión de un Equipo o Club. Normalmente es del cuerpo técnico o de la junta, pero puede ser un aficionado. Quiere preparar partidos y que su Equipo se vea bien. En el futuro será quien pague un Plan.
- **Administrador**: Luis. Aprueba o rechaza Solicitudes de gestión, activa Planes a mano (en el futuro) y modera.

### 3.2 Jobs To Be Done

- **Seguidor:** saber cuándo y dónde es el próximo partido; enterarse del resultado sin buscarlo en fcf.cat; ver cómo va el Equipo en la liga; ver sus propios números (jugador) o los de su hijo (familia).
- **Gestor:** preparar el próximo partido conociendo al rival en minutos y no en horas; compartir ese análisis solo con su cuerpo técnico; que la app muestre bien la marca de su Equipo.
- **Administrador:** controlar quién accede a los Dossiers de cada Equipo.

### 3.3 User Journeys clave

- **UJ-1, seguir un Equipo.** Marc, jugador del Guinardó A, recibe el enlace por el grupo de WhatsApp. Entra en la web sin Cuenta, busca "Guinardó" y ve los Equipos del Club (A, B, juveniles…). Sigue el Guinardó A. **Clímax:** sin registrarse, el Feed ya le muestra "Darna 2019 – Guinardó, sábado 24/10, 20:15, Mpal. Parc Catalana" y el último resultado (5-0). Instala la app en el móvil. *Edge case:* busca un nombre que no existe y la app le dice que no hay resultados y le sugiere buscar por el nombre del Club.
- **UJ-2, después del partido.** El sábado por la noche, como mucho una hora después de que la FCF publique el Acta, Marc ve el resultado en el Feed. Entra en la Ficha de partido: goles con minuto, tarjetas, alineaciones, cambios y árbitro. Después abre su Ficha de jugador: convocatorias, titularidades, goles y tarjetas. **Clímax:** ve su gol y su racha de titularidades sin pasar por fcf.cat. Si tiene Cuenta, le llega el aviso "resultado publicado". *Edge case:* el partido se aplaza; el Feed lo marca como aplazado y, si tiene Cuenta, recibe el aviso.
- **UJ-3, preparar al rival.** Luis tiene Cuenta y ha pedido ser Gestor del Guinardó A; el Administrador lo ha aprobado. El lunes abre el próximo partido y pide el Dossier del rival. **Clímax:** en minutos tiene la forma del rival, quién marca primero, goles por Tramo, el once más repetido, la plantilla con la tabla de convocatorias, las sanciones y los debutantes. Comparte el Enlace privado con su cuerpo técnico. Nadie del rival puede verlo. *Edge case:* el rival aún no ha jugado ningún partido; el Dossier lo indica en lugar de mostrar estadísticas vacías.
- **UJ-4, varios Equipos.** Núria sigue el Guinardó A y el Alevín A. El Feed mezcla los partidos de ambos, y cada tarjeta lleva los colores de su Equipo. Al entrar en el Alevín, toda la app adopta su Tema y los niños aparecen con iniciales y dorsal.
- **UJ-5, aprobar un Gestor.** Luis, como Administrador, recibe una Solicitud de gestión para un Equipo, ve quién la pide y para qué Equipo, y la aprueba o la rechaza. Quien la pidió se entera del resultado.

## 4. Glosario

- **Club** — Entidad federada en la FCF (p. ej. Guinardó C.F.). Tiene uno o varios Equipos.
- **Equipo** — Conjunto inscrito por un Club en una Competición de una Temporada (p. ej. "Guinardó C.F. A"). Pertenece a un único Club. Es la unidad que se sigue.
- **Disciplina** — Modalidad de la FCF. En v1: Futbol 11, Futbol 7 y Futbol Femení.
- **Temporada** — Año deportivo de la FCF (p. ej. 2026-2027). La v1 muestra la Temporada en curso.
- **Competición** — Torneo de la FCF dentro de una Disciplina (p. ej. Quarta Catalana). En v1 solo se tiene en cuenta la liga de cada Equipo.
- **Grupo** — División de una Competición con su propia clasificación (p. ej. Grup 20). Un Equipo juega la liga en un Grupo.
- **Jornada** — Ronda numerada de partidos de un Grupo.
- **Partido** — Encuentro entre dos Equipos de un Grupo en una Jornada. Puede estar programado, aplazado o jugado.
- **Acta** — Registro oficial de un Partido jugado que publica la FCF: resultado, alineaciones, goles, tarjetas, cambios, árbitros, técnicos.
- **Resultado de despacho** — Resultado que fija la FCF por decisión de su comité y que sustituye al del campo (p. ej. por alineación indebida).
- **Convocado / Titular / Suplente** — Situación de un Jugador en el Acta de un Partido. No convocado = no aparece en el Acta.
- **Jugador** — Persona que aparece en Actas de un Equipo en la Temporada.
- **Categoría de menores** — Competición de fútbol base (juvenil, cadete, infantil, alevín, benjamín, prebenjamín). En ellas los Jugadores se muestran Anonimizados.
- **Anonimizado** — Jugador mostrado solo con iniciales y dorsal (p. ej. "D. A. #8").
- **Equipo seguido** — Equipo que un usuario ha decidido seguir.
- **Feed** — Pantalla de inicio con los Partidos y resultados de todos los Equipos seguidos.
- **Tema** — Colores y escudo con que la app se presenta para un Equipo. Por defecto salen de la FCF (equipación y escudo).
- **Marca** — Tema ajustado a mano por un Gestor, más enlaces a sus redes.
- **Tramo** — Cada una de las 6 partes iguales en que se divide la duración de un Partido para las estadísticas de goles.
- **Estadísticas avanzadas** — Métricas de un Equipo calculadas a partir de todas sus Actas de la Temporada: quién marca primero, goles por Tramo, once más repetido, debutantes, sanciones vigentes.
- **Dossier** — Informe de un rival concreto, generado bajo petición de un Gestor, con Estadísticas avanzadas y plantilla. Solo lo ven los Gestores del Equipo que lo pidió.
- **Enlace privado** — Dirección web de un Dossier que solo abre quien la recibe.
- **Cuenta** — Registro de un usuario en la app. Es opcional para el Seguidor y obligatoria para el Gestor y el Administrador.
- **Solicitud de gestión** — Petición de un usuario con Cuenta para ser Gestor de un Equipo o Club. La aprueba o rechaza el Administrador.
- **Plan** — (futuro) Derecho de pago que desbloquea funciones para un Equipo o un Club entero. En v1 no existe pago.

## 5. Features

### 5.1 Búsqueda y seguimiento de Equipos

**Descripción:** cualquier persona, con o sin Cuenta, busca un Club o Equipo de la FCF por nombre y sigue uno o varios Equipos. Al seguir un Equipo, el Feed y la Ficha de equipo funcionan de inmediato con los datos de toda la Temporada en curso, sin alta manual de nadie. Realiza UJ-1 y UJ-4.

#### FR-1: Buscar Clubs y Equipos
El Seguidor puede buscar por nombre un Club o Equipo de cualquier Disciplina de la v1. Realiza UJ-1.

**Consecuencias (testeables):**
- Con 3 o más caracteres, la búsqueda devuelve Clubs cuyo nombre coincide, ignorando acentos y mayúsculas ("guinardo" encuentra "GUINARDÓ, C.F.").
- Al elegir un Club se listan sus Equipos de la Temporada en curso de Futbol 11, Futbol 7 y Futbol Femení, con su Competición y Grupo de liga.
- Sin resultados, la app lo dice y sugiere buscar por el nombre del Club.

**Fuera de alcance:**
- Buscar Jugadores, árbitros o campos.

#### FR-2: Seguir y dejar de seguir
El Seguidor puede seguir y dejar de seguir Equipos sin Cuenta. Realiza UJ-1.

**Consecuencias (testeables):**
- Sin Cuenta, los Equipos seguidos se guardan en el dispositivo y siguen ahí al reabrir la app.
- Con Cuenta, los Equipos seguidos se sincronizan entre dispositivos. Al crear la Cuenta, los Equipos seguidos sin Cuenta en ese dispositivo pasan a la Cuenta.
- No hay límite práctico de Equipos seguidos. `[ASSUMPTION: sin límite en v1]`

### 5.2 Feed

**Descripción:** pantalla de inicio que mezcla, en orden cronológico, los Partidos próximos y los resultados recientes de todos los Equipos seguidos, al estilo Sofascore. Cada tarjeta lleva el Tema de su Equipo. Realiza UJ-1, UJ-2 y UJ-4.

#### FR-3: Feed mezclado
El Seguidor ve en el Feed los Partidos de todos sus Equipos seguidos. Realiza UJ-1 y UJ-4.

**Consecuencias (testeables):**
- Cada Equipo seguido aporta como mínimo su próximo Partido y su último resultado.
- Cada tarjeta muestra: Equipos, escudos, fecha, hora, campo, Jornada y, si se ha jugado, el resultado.
- Los Partidos aplazados se marcan como "aplazado"; los Resultados de despacho muestran el resultado oficial y se indica que fue de despacho.
- Cada tarjeta usa los colores del Tema de su Equipo seguido.
- Sin Equipos seguidos, el Feed invita a buscar uno (FR-1).

### 5.3 Ficha de equipo

**Descripción:** todo lo de un Equipo en su liga: resumen, calendario y resultados, clasificación. Al entrar, la app adopta el Tema del Equipo. Realiza UJ-1, UJ-2 y UJ-4.

#### FR-4: Resumen del Equipo
El Seguidor ve el resumen de un Equipo: próximo Partido, último resultado, posición en el Grupo, puntos, partidos jugados, goles a favor y en contra, y racha de los últimos 5 Partidos (G/E/P). Realiza UJ-1.

**Consecuencias (testeables):**
- Los datos coinciden con los publicados por la FCF para ese Grupo y Temporada.
- Si el Equipo tiene un Partido pendiente de una Jornada anterior, aparece como próximo Partido según su fecha.

#### FR-5: Calendario y resultados
El Seguidor ve todos los Partidos de liga del Equipo en la Temporada, por Jornada: rival, casa o fuera, fecha, hora, campo y resultado. Realiza UJ-2.

**Consecuencias (testeables):**
- Los Partidos aplazados se muestran como pendientes con su nueva fecha si la hay.
- Los Resultados de despacho muestran el resultado oficial y, si se conoce, el del campo (como "3-0*, en el campo 0-1").
- Al tocar un Partido jugado se abre su Ficha de partido (FR-7).

#### FR-6: Clasificación del Grupo
El Seguidor ve la clasificación del Grupo del Equipo: posición, puntos, PJ, G, E, P, GF, GC, diferencia y racha, con el Equipo destacado. Realiza UJ-1.

**Consecuencias (testeables):**
- Se marcan las posiciones de ascenso y descenso cuando la FCF las indica.
- Al tocar otro Equipo de la clasificación se abre su Ficha de equipo.

### 5.4 Ficha de partido

**Descripción:** el Acta de un Partido presentada de forma clara. Realiza UJ-2.

#### FR-7: Ver el Acta
El Seguidor ve, para un Partido jugado: resultado, fecha, campo, Jornada, árbitros, alineaciones de ambos Equipos (Titulares y Suplentes, con capitán y portero), goles con minuto y tipo, tarjetas con minuto, cambios y cuerpo técnico. Realiza UJ-2.

**Consecuencias (testeables):**
- Un Partido sin Acta publicada muestra los datos de programación y el texto "acta pendiente de publicar".
- Los Jugadores de Categorías de menores aparecen Anonimizados (FR-17).
- Al tocar un Jugador se abre su Ficha de jugador (FR-9).

### 5.5 Plantilla y Jugadores

**Descripción:** quién juega en el Equipo y cómo le va a cada uno, calculado a partir de todas las Actas de liga de la Temporada. Realiza UJ-2.

#### FR-8: Plantilla con estadísticas
El Seguidor ve la plantilla del Equipo: todos los Jugadores que han aparecido en alguna Acta, con dorsal, convocatorias, titularidades, goles, tarjetas amarillas y rojas, y una tabla por Jornada con Titular / Suplente / No convocado. Realiza UJ-2.

**Consecuencias (testeables):**
- Se indica el capitán y el portero cuando el Acta lo marca.
- Se puede ordenar por cada columna.
- Un Jugador que debuta en el último Partido se destaca como debutante.

#### FR-9: Ficha de jugador
El Seguidor ve la ficha de un Jugador: totales de la Temporada (convocatorias, titularidades, goles, tarjetas, sanciones) y la lista de sus Partidos con su participación. Realiza UJ-2.

**Consecuencias (testeables):**
- Los totales coinciden con la suma de las Actas de la Temporada.
- Si es de una Categoría de menores, se muestra Anonimizado (FR-17).

### 5.6 Rankings del Grupo

**Descripción:** tablas de todo el Grupo, abiertas a todos.

#### FR-10: Goleadores
El Seguidor ve el ranking de goleadores del Grupo, con Equipo y goles de penalti.

#### FR-11: Joc net
El Seguidor ve la clasificación de juego limpio del Grupo (amarillas, dobles amarillas, rojas, sanciones).

#### FR-12: Sanciones
El Seguidor ve las sanciones del comité que afectan al Grupo, por Jornada.

**Consecuencias (testeables, FR-10 a FR-12):**
- Los datos coinciden con los de la FCF para el Grupo y la Temporada.
- En Categorías de menores, los Jugadores aparecen Anonimizados.

### 5.7 Estadísticas avanzadas

**Descripción:** lo que hoy Luis calcula a mano en su dossier, disponible para cualquier Equipo en su Ficha de equipo y abierto a todos los Seguidores. Se calcula con todas las Actas de liga de la Temporada. Realiza UJ-3 (como base del Dossier).

#### FR-13: Quién marca primero
El Seguidor ve en cuántos Partidos jugados marcó primero el Equipo y cuántos de esos ganó.

#### FR-14: Goles por Tramo
El Seguidor ve los goles a favor y en contra del Equipo repartidos en 6 Tramos iguales de la duración del Partido.

**Consecuencias (testeables):**
- En un Partido de 90 minutos los Tramos son 0-15, 16-30, 31-45, 46-60, 61-75 y 76-90 (los goles en el añadido cuentan en el último Tramo de su parte).
- En categorías con Partidos más cortos, los Tramos se ajustan a su duración, de modo que se pueden comparar Equipos de distintas categorías.

#### FR-15: Once más repetido
El Seguidor ve los 11 Jugadores (7 en Futbol 7) con más titularidades, con su dorsal, titularidades sobre Partidos jugados, goles y si es capitán o portero.

#### FR-16: Sanciones vigentes de Jugadores
El Seguidor ve qué Jugadores del Equipo tienen una sanción pendiente de cumplir y cuántos Partidos les quedan. `[ASSUMPTION: se deduce del texto de las sanciones de la FCF y de los Partidos jugados desde entonces; si no se puede deducir con certeza, se muestra la sanción sin el contador]`

### 5.8 Categorías de menores

#### FR-17: Anonimizar a menores
En las Categorías de menores, la app muestra a los Jugadores Anonimizados (iniciales y dorsal) en todas las pantallas, rankings, notificaciones y Dossiers. Las estadísticas se mantienen. Realiza UJ-4.

**Consecuencias (testeables):**
- "ARUMÍ VALLALTA, QUIM" en una Categoría de menores se ve como "Q. A. V." o similar, nunca con el nombre completo.
- La regla se aplica según la Competición, no según la edad de cada Jugador (la FCF no la publica).
- `[ASSUMPTION: los Gestores de un Equipo de una Categoría de menores ven los nombres completos de su propio Equipo, nunca los del rival]`

### 5.9 Tema y Marca

**Descripción:** la app se viste con los colores del Equipo. Realiza UJ-4.

#### FR-18: Tema automático
Cada Equipo tiene un Tema por defecto con su escudo y los colores de su primera equipación tal como los publica la FCF.

**Consecuencias (testeables):**
- Cualquier Equipo de la v1 tiene Tema sin intervención humana.
- Con colores de poco contraste (p. ej. camiseta blanca), la app sigue siendo legible: el Tema nunca deja texto ilegible.

#### FR-19: Marca manual (Hito 2)
El Gestor puede ajustar la Marca de su Equipo: logo, colores principales y enlaces a sus redes sociales. Sustituye al Tema automático para todos los Seguidores de ese Equipo.

**Fuera de alcance:**
- Sacar la Marca automáticamente de redes sociales (post-MVP).

### 5.10 Cuentas, roles y Solicitudes de gestión (Hito 2)

**Descripción:** la Cuenta es opcional para seguir Equipos y necesaria para recibir notificaciones y ser Gestor. Este modelo de roles es el que admitirá el pago en el futuro. Realiza UJ-3 y UJ-5.

#### FR-20: Cuenta opcional
Cualquier usuario puede crear una Cuenta para sincronizar Equipos seguidos (FR-2), recibir notificaciones (§5.12) y enviar Solicitudes de gestión.

#### FR-21: Solicitud de gestión
Un usuario con Cuenta puede pedir ser Gestor de un Equipo o de un Club entero, indicando su relación con él. Realiza UJ-3.

**Consecuencias (testeables):**
- La Solicitud queda pendiente hasta que el Administrador decide.
- Quien la pidió ve su estado (pendiente, aprobada, rechazada) y recibe aviso cuando cambia.
- Un Gestor de un Club entero es Gestor de todos sus Equipos.
- Un Equipo puede tener varios Gestores. `[ASSUMPTION: todo el cuerpo técnico puede ser Gestor]`

#### FR-22: Aprobar o rechazar Solicitudes
El Administrador ve las Solicitudes pendientes (quién, qué Equipo o Club, relación declarada) y las aprueba o rechaza. También puede retirar el rol de Gestor. Realiza UJ-5.

#### FR-23: Preparado para Planes
El modelo de roles permite, sin rehacerlo, que en el futuro un Plan de pago por Equipo o por Club desbloquee funciones. En la v1 no hay pago ni Planes visibles. La aprobación de la Solicitud de gestión es el punto donde irá el pago.

### 5.11 Dossier (Hito 2)

**Descripción:** el dossier que hoy Luis hace a mano, generado por la app para un rival concreto. Realiza UJ-3.

#### FR-24: Pedir un Dossier
El Gestor puede pedir el Dossier del rival de cualquier Partido de liga de su Equipo. Realiza UJ-3.

**Consecuencias (testeables):**
- El Dossier está disponible en minutos.
- Si el rival no ha jugado ningún Partido, el Dossier lo indica en lugar de mostrar estadísticas vacías.

#### FR-25: Contenido del Dossier
El Dossier del rival incluye: posición, puntos, goles y racha; resultados por Jornada (casa o fuera, aplazados, Resultados de despacho); quién marca primero; goles por Tramo a favor y en contra; once más repetido; plantilla con tabla por Jornada; goleadores; sanciones vigentes; debutantes del último Partido; y el próximo Partido (fecha, hora, campo, casa o fuera). Incluye también la clasificación del Grupo con el propio Equipo y el rival destacados.

**Fuera de alcance:**
- Las "Claves" (análisis narrativo escrito por IA): post-MVP.

#### FR-26: Visibilidad del Dossier
Solo los Gestores del Equipo que pidió el Dossier pueden verlo. Ningún Seguidor, ni Gestor de otro Equipo, ni el propio rival.

#### FR-27: Compartir por Enlace privado
El Gestor puede generar un Enlace privado del Dossier para compartirlo con su cuerpo técnico. `[ASSUMPTION: quien tiene el enlace lo abre sin Cuenta; el Gestor puede revocarlo; caduca al terminar el Partido]`

### 5.12 Notificaciones (Hito 2)

**Descripción:** avisos a usuarios con Cuenta sobre sus Equipos seguidos. En iPhone requieren tener la app instalada.

#### FR-28: Resultado publicado
Aviso cuando la FCF publica el resultado o el Acta de un Partido de un Equipo seguido. Realiza UJ-2.

#### FR-29: Cambio de Partido
Aviso cuando cambia la fecha, la hora o el campo de un próximo Partido, o se aplaza.

#### FR-30: Recordatorio de Partido
Aviso antes del Partido con hora y campo. `[ASSUMPTION: el mismo día, 3 horas antes]`

#### FR-31: Sanción de un Jugador
Aviso cuando el comité sanciona a un Jugador de un Equipo seguido (Anonimizado si es de una Categoría de menores).

**Consecuencias (testeables, FR-28 a FR-31):**
- El usuario puede activar o desactivar cada tipo de aviso por Equipo seguido.
- No se envía el mismo aviso dos veces.

### 5.13 Idioma, frescura y fuente

#### FR-32: Catalán y castellano
La interfaz está en catalán y en castellano, a elección del usuario. Los datos de la FCF (nombres de Equipos, Competiciones, textos de sanciones) se muestran tal como vienen, sin traducir.

#### FR-33: Frescura de los datos
Un resultado, un Acta, un cambio de Partido o una sanción publicados por la FCF aparecen en la app en una hora como máximo.

#### FR-34: Atribución
La app indica que los datos proceden de la FCF y que no es una app oficial de la FCF.

## 6. Non-Goals (explícitos)

- No hay resultados en directo: la app muestra lo que publica la FCF, cuando lo publica.
- No es una app oficial de la FCF ni lo aparenta.
- No hay contenido de usuarios: ni fotos, ni crónicas, ni convocatorias propias.
- No gestiona el club: ni fichas, ni cuotas, ni entrenamientos.
- No hay apuestas ni chat.
- No hay copas, fases de ascenso ni amistosos: solo la liga.
- No hay pago en v1.
- No es una app nativa de tiendas: es una PWA.

## 7. Alcance del MVP

### 7.1 Dentro

**Hito 1, "el Guinardó la usa"** (Seguidor sin Cuenta):
- 5.1 Búsqueda y seguimiento (FR-1, FR-2 sin sincronización)
- 5.2 Feed
- 5.3 Ficha de equipo
- 5.4 Ficha de partido
- 5.5 Plantilla y Jugadores
- 5.6 Rankings del Grupo
- 5.7 Estadísticas avanzadas
- 5.8 Categorías de menores
- 5.9 Tema automático (FR-18)
- 5.13 Idioma, frescura y fuente

**Primera entrega (23/10/2026):** un subconjunto del Hito 1 solo para el Guinardó A: resumen, calendario y resultados, clasificación, Fichas de partido y plantilla con estadísticas. Se definirá en su propia spec.

**Hito 2, "listo para otros clubs":**
- 5.10 Cuentas, roles y Solicitudes de gestión (FR-20 a FR-23) y la sincronización de FR-2
- 5.11 Dossier con Enlace privado
- 5.12 Notificaciones
- 5.9 Marca manual (FR-19)

### 7.2 Fuera del MVP

- **Pasarela de pago y Planes:** v1 gratis; el modelo de roles ya los admite (FR-23).
- **"Claves" escritas por IA en el Dossier:** se aplazan por decisión de Luis. `[NOTA PM]` Es lo que más valor tiene del dossier manual; conviene que sea lo primero tras el MVP.
- **Marca desde redes sociales:** frágil (bloqueos, condiciones de uso de Instagram y X) y la FCF no da las cuentas de cada club.
- **Copas y fases de ascenso:** la v1 se centra en la liga.
- **Futbol 5, Futbol Sala, Futbol Sala Femení, Futbol Platja:** fuera por decisión de alcance.
- **Mapa del campo y compartir como imagen:** propuestos y descartados para v1.
- **Temporadas anteriores:** la v1 muestra solo la Temporada en curso.

## 8. Métricas de éxito

- **SM-1:** el cuerpo técnico del Guinardó A usa la app cada semana para preparar el partido, en lugar de fcf.cat y del dossier hecho a mano. Objetivo: 4 Jornadas seguidas tras el Hito 2. Valida FR-24 a FR-27.
- **SM-2:** 20 Seguidores del Guinardó (plantilla y cuerpo técnico del primer equipo) siguen el Equipo en el primer mes tras el Hito 1. Valida FR-1 a FR-3.
- **SM-3:** preparar un rival pasa de horas a menos de 10 minutos. Valida FR-24 y FR-25.
- **Counter-metric SM-4:** cero discrepancias entre la app y la FCF en resultados, clasificación y Actas detectadas por usuarios. Optimizar la velocidad no puede costar exactitud. Valida FR-33.

## 9. Preguntas abiertas

1. ¿Permite la FCF reutilizar sus datos? Ver Q-1 en `client-questions.md`.
2. ¿Qué opina el Guinardó de mostrar datos de sus equipos base, aunque estén Anonimizados? Ver Q-2 en `client-questions.md`.
3. (Interna) Duración de los Partidos por categoría para calcular los Tramos (FR-14): sale de la normativa de la FCF o de los minutos de las Actas. Se resuelve en la spec.
4. (Interna) Cómo identificar una Categoría de menores a partir del nombre de la Competición (FR-17). Se resuelve en la spec.
5. (Interna) Con qué retraso publica la FCF el resultado tras el Partido; afecta a lo que el usuario puede esperar en UJ-2.

## 10. Índice de Assumptions

| # | Assumption | Default propuesto | Confirma |
|---|---|---|---|
| A-1 | Límite de Equipos seguidos (FR-2) | Sin límite en v1 | Luis |
| A-2 | Sanciones vigentes (FR-16) | Se deducen de la FCF; sin contador si no hay certeza | Luis |
| A-3 | Gestores de menores (FR-17) | Ven nombres completos de su propio Equipo, nunca los del rival | Luis |
| A-4 | Varios Gestores por Equipo (FR-21) | Sí, todo el cuerpo técnico | Luis |
| A-5 | Enlace privado del Dossier (FR-27) | Se abre sin Cuenta, revocable, caduca al terminar el Partido | Luis |
| A-6 | Momento del recordatorio (FR-30) | El mismo día, 3 horas antes | Luis |
