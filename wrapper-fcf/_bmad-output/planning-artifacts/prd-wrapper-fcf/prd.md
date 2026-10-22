---
title: Wrapper FCF
client: Sinoficina (producto propio)
status: final # draft | final
created: 2026-10-22
updated: 2026-10-22
---

# PRD: Wrapper FCF

## 0. Propósito del documento

Este PRD define qué construimos en la v1 de Wrapper FCF. Lo leen Luis (dueño del producto), el equipo de Sinoficina y los agentes que implementarán cada parte. Se basa en:
- la entrevista de producto del 22/10/2026 y la revisión posterior, registradas en `.decision-log.md`;
- el dossier "Guinardó: rivales Grup 20" que Luis hizo a mano (`materials/guinardo-dossier.html`);
- la ingeniería inversa de la API interna de fcf.cat (`fcf/ENDPOINTS.md`);
- tres revisiones del borrador (`review-*.md`).

Cada feature de §5 se convertirá en una spec de implementación con `nch-spec`. El PRD describe capacidades, no tecnología.

## 1. Visión

Wrapper FCF es la forma cómoda de seguir a un **Equipo** de la Federació Catalana de Futbol. La web oficial (fcf.cat) tiene todos los datos, pero cuesta encontrarlos, no se adapta al móvil y no saca conclusiones. Wrapper FCF coge esos datos públicos y los presenta como una app de resultados moderna, al estilo de Sofascore: buscas tu Equipo, lo sigues, y tienes su calendario, resultados, clasificación, Actas, Plantilla y Estadísticas avanzadas, con los colores de tu Equipo.

Encima de eso, la app hace lo que hoy Luis hace a mano cada semana: preparar al rival. Un **Gestor** pide el **Dossier** del rival y en minutos lo tiene todo en una vista, comparado con su propio Equipo y compartido solo con su cuerpo técnico.

La app nace para el Guinardó C.F., pero cualquier Equipo de la FCF puede usarla desde el primer día sin alta manual. Las Estadísticas avanzadas son gratis para todos. En el futuro, un **Plan** de pago desbloqueará el Dossier, la Marca manual y las Claves escritas por IA.

## 2. Contexto del encargo

- **Producto propio de Sinoficina**, sin cliente externo. Luis decide el producto. Las incógnitas que dependen de terceros (permiso de la FCF, datos de menores) están en `client-questions.md`.
- **Tipo de proyecto:** MVP de validación con el propio club, construido para abrirse a cualquier club de la FCF sin rehacerlo.
- **Entrega en dos hitos** (ver §7):
  - **Hito 1, "el Guinardó la usa":** seguimiento y estadísticas, sin Cuentas.
  - **Hito 2, "listo para otros clubs":** Cuentas, roles, Dossier, notificaciones y Marca manual.
- **Urgencia:** Luis quiere la Primera entrega (§7.1) online el 23/10/2026, antes de Darna 2019 – Guinardó (sábado 24/10, 20:15). Ha decidido cerrar primero este PRD aunque eso ponga en riesgo esa fecha.
- **Datos:** dependemos al 100 % de la API interna, pública y no documentada de fcf.cat. Puede cambiar sin aviso. Esa API también trae datos que la app nunca muestra: teléfonos de los responsables de los clubs y horarios de entrenamiento.
- **Presupuesto:** planes gratuitos de la infraestructura.
- **Restricciones técnicas** (decididas por Luis, se aplican en las specs): React + Supabase + Vercel, PWA.

## 3. Usuarios

### 3.1 Roles

- **Seguidor**: cualquier persona que sigue Equipos (jugadores, cuerpo técnico, familias, aficionados). No necesita Cuenta.
- **Gestor**: persona con Cuenta a la que se ha aprobado una Solicitud de gestión de un Equipo o de un Club entero. Suele ser del cuerpo técnico o de la junta. Pide Dossiers y ajusta la Marca. En el futuro será quien pueda pagar un Plan, aunque puede pagarlo cualquier usuario con Cuenta.
- **Administrador**: Luis. Aprueba al primer Gestor de cada Equipo o Club, modera la Marca y la anonimización, y en el futuro gestionará los Planes. También puede ser Gestor.

### 3.2 Jobs To Be Done

- **Seguidor:** saber cuándo y dónde es el próximo Partido; enterarse del resultado sin buscarlo en fcf.cat; ver cómo va el Equipo en la liga; ver sus propios números o los de su hijo.
- **Gestor:** preparar el próximo Partido conociendo al rival en minutos y no en horas; que ese análisis no llegue al rival; que la app muestre bien la marca de su Equipo.
- **Administrador:** controlar quién es Gestor de cada Equipo; proteger los datos de los menores.

### 3.3 User Journeys clave

- **UJ-1, seguir un Equipo.** Marc, jugador del Guinardó A, recibe el enlace por el grupo de WhatsApp. Entra sin Cuenta, busca "guinardo" y ve el Club y sus Equipos. Sigue el Guinardó A. **Clímax:** sin registrarse, el Feed ya le muestra "Darna 2019 – Guinardó, sábado 24/10, 20:15, Mpal. Parc Catalana" y el último resultado (1-1 con el Torre Fuerte). Instala la app en el móvil. *Edge case:* busca un nombre que no existe y la app le sugiere buscar por el nombre del Club.
- **UJ-2, después del Partido.** El sábado por la noche, como mucho una hora después de que la FCF publique el resultado, Marc lo ve en el Feed. Entra en la Ficha de partido: goles con minuto, tarjetas, alineaciones, cambios y árbitro. Después abre su Ficha de jugador. **Clímax:** ve su gol y sus titularidades sin pasar por fcf.cat. Si tiene Cuenta, le llega el aviso "resultado publicado". *Edge case:* el Acta aún no está cerrada y el resultado aparece como "provisional"; si la FCF lo corrige, recibe "resultado modificado".
- **UJ-3, preparar al rival.** Luis pide ser Gestor del Guinardó A; como es el primero, el Administrador lo verifica y lo aprueba. El lunes abre la lista de próximos rivales y pide el Dossier del Darna. **Clímax:** en minutos tiene, en una vista, la forma del rival, quién marca primero, goles por Tramo, el once más repetido, la Plantilla con la tabla de convocatorias, las sanciones vigentes, los debutantes y los totales de tarjetas, junto a la ficha de su propio Equipo. Comparte el enlace con su entrenador, que también es Gestor. Si alguien lo reenvía al rival, no lo puede abrir. Hasta el inicio del Partido, el Dossier se actualiza solo y muestra "Datos FCF a…". *Edge case:* el rival aún no ha jugado ningún Partido válido; el Dossier lo dice en lugar de mostrar estadísticas vacías.
- **UJ-4, varios Equipos.** Núria sigue el Martinenc B y el Martinenc Aleví A. El Feed mezcla los Partidos de ambos, cada tarjeta con los colores de su Equipo. Al entrar en el Aleví, toda la app adopta su Tema, y los niños y el árbitro aparecen Anonimizados.
- **UJ-5, aprobar Gestores.** Llega una Solicitud de gestión para un Equipo sin Gestores: el Administrador comprueba quién es y la aprueba o la rechaza. Si el Equipo ya tiene Gestores, son ellos quienes reciben y deciden la Solicitud. Quien la pidió se entera del resultado.

## 4. Glosario

- **Club** — Entidad federada en la FCF (p. ej. Guinardó C.F.). Tiene uno o varios Equipos.
- **Equipo** — Inscripción de un Club en una categoría con una letra (p. ej. "Guinardó C.F. A", "Martinenc Aleví A"). Pertenece a un único Club. Conserva su identidad entre Temporadas y fases. Es la unidad que se sigue.
- **Disciplina** — Modalidad de la FCF. En v1: Futbol 11, Futbol 7 y Futbol Femení.
- **Temporada** — Año deportivo de la FCF (p. ej. 2026-2027).
- **Competición** — Torneo de la FCF dentro de una Disciplina (p. ej. Quarta Catalana, Segona Divisió Aleví S12).
- **Liga** — Competición con clasificación por Grupo que no es una copa, un torneo ni una promoción o fase de ascenso. Es lo único que cubre la v1. Puede tener varias fases.
- **Grupo** — División de una Liga con su propia clasificación (p. ej. Grup 20). En cada fase, un Equipo juega en un Grupo.
- **Jornada** — Ronda numerada de Partidos de un Grupo. En Grupos impares, un Equipo descansa en algunas.
- **Partido** — Encuentro de Liga entre dos Equipos en una Jornada. Estados: programado, aplazado (con o sin nueva fecha), jugado.
- **Acta** — Registro oficial de un Partido jugado que publica la FCF. Mientras la FCF no la cierra, su resultado es **provisional**.
- **Resultado de despacho** — Resultado que fija el comité de la FCF y que sustituye al del campo. La app lo detecta cuando el resultado oficial no coincide con los goles del Acta.
- **Partido válido** — Partido jugado cuyo resultado no es de despacho. Solo los Partidos válidos cuentan para las Estadísticas avanzadas.
- **Jugador** — Persona que aparece en Actas de un Equipo en la Temporada.
- **Convocado / Titular / Suplente / No convocado** — Situación de un Jugador en un Partido de su Equipo según el Acta. No convocado = no aparece en ella.
- **Debutante** — Jugador cuya primera aparición en un Acta del Equipo en la Temporada es el último Partido jugado por el Equipo.
- **Plantilla** — Jugadores de un Equipo en la Temporada con sus estadísticas.
- **Racha** — Resultados (G/E/P) de los últimos 5 Partidos jugados.
- **Categoría de menores** — Competición de fútbol base (juvenil, cadete, infantil, alevín, benjamín, prebenjamín, y sus equivalentes femeninos). Ante la duda, una Competición se trata como Categoría de menores.
- **Anonimizado** — Persona mostrada solo con iniciales del nombre y del primer apellido y, si es Jugador, el dorsal (p. ej. "Q. A. #21").
- **Equipo seguido** — Equipo que un usuario sigue.
- **Feed** — Pantalla de inicio con los Partidos de todos los Equipos seguidos.
- **Ficha de equipo / Ficha de partido / Ficha de jugador** — Pantallas de detalle de un Equipo, un Partido y un Jugador.
- **Tema** — Colores y escudo con los que la app se presenta para un Equipo. Por defecto salen de la FCF.
- **Marca** — Tema ajustado a mano por un Gestor (logo que sustituye al escudo, colores) más enlaces a sus redes.
- **Tramo** — Cada una de las 6 partes iguales en que se divide la duración de un Partido para contar goles.
- **Estadísticas avanzadas** — Métricas de un Equipo calculadas con sus Partidos válidos de la fase: quién marca primero, goles por Tramo, once más repetido, sanciones vigentes. Gratis y abiertas a todos.
- **Dossier** — Informe de un rival concreto para un Partido de Liga, pedido por un Gestor. Solo lo ven los Gestores de su Equipo.
- **Cuenta** — Registro de un usuario. Es opcional para el Seguidor y obligatoria para Gestores y Administrador.
- **Solicitud de gestión** — Petición de un usuario con Cuenta para ser Gestor de un Equipo o Club.
- **Notificación** — Aviso que la app envía a un usuario con Cuenta.
- **Plan** — (futuro) Derecho de pago, por Equipo o por Club, que desbloquea Dossier, Marca manual y Claves. En v1 no existe pago.
- **Claves** — (futuro) Análisis narrativo del rival escrito por IA.

## 5. Features

### 5.1 Búsqueda y seguimiento

**Descripción:** cualquier persona busca un Club y sigue uno o varios de sus Equipos. Al seguir un Equipo, el Feed y su Ficha de equipo funcionan con toda la Temporada en curso, sin alta manual de nadie. Realiza UJ-1 y UJ-4.

#### FR-1: Buscar Clubs y ver sus Equipos
El Seguidor puede buscar un Club por nombre y ver sus Equipos. Realiza UJ-1.

**Consecuencias (testeables):**
- Con 3 o más caracteres, la búsqueda devuelve los Clubs cuyo nombre coincide, sin distinguir acentos ni mayúsculas ("guinardo" encuentra "GUINARDO, C.F.").
- Al elegir un Club se listan sus Equipos de Futbol 11, Futbol 7 y Futbol Femení con su categoría, agrupados por categoría.
- Sin resultados, la app lo dice y sugiere probar otra parte del nombre del Club.

**Fuera de alcance:** buscar Jugadores, árbitros o campos.

#### FR-2: Seguir y dejar de seguir
El Seguidor puede seguir y dejar de seguir Equipos sin Cuenta. Realiza UJ-1.

**Consecuencias (testeables):**
- Tras seguir un Equipo, su próximo Partido y su último resultado aparecen en el Feed en menos de 1 minuto.
- Sin Cuenta, los Equipos seguidos se guardan en el dispositivo; si el usuario borra los datos del navegador, se pierden.
- Con Cuenta, se sincronizan entre dispositivos; al iniciar sesión, los Equipos seguidos en el dispositivo se suman a los de la Cuenta.
- Sin límite de Equipos seguidos.
- El seguimiento sigue al Equipo cuando cambia de Grupo (nueva fase) o de Temporada.

### 5.2 Feed

**Descripción:** pantalla de inicio con los Partidos próximos y recientes de todos los Equipos seguidos. Realiza UJ-1, UJ-2 y UJ-4.

#### FR-3: Feed de próximos y recientes
El Seguidor ve en el Feed los Partidos de sus Equipos seguidos. Realiza UJ-1 y UJ-4.

**Consecuencias (testeables):**
- Arriba, los Partidos de los próximos 7 días, el más cercano primero; debajo, los resultados de los últimos 7 días, el más reciente primero.
- Si un Equipo seguido no tiene Partidos en esas ventanas, aporta igualmente su próximo Partido y su último resultado.
- Un Partido entre dos Equipos seguidos aparece una sola vez.
- Cada tarjeta muestra Equipos, escudos, fecha, hora, campo, Jornada y, si se ha jugado, el resultado. Lleva los colores del Tema del Equipo seguido (si son dos, los del local).
- Los aplazados se marcan "aplazado" (con la nueva fecha o "sin fecha"); los resultados sin Acta cerrada, "provisional"; los Resultados de despacho, "despacho".
- Sin Equipos seguidos, el Feed invita a buscar uno (FR-1). En verano, sin Partidos, muestra el último resultado de la Temporada acabada.

### 5.3 Ficha de equipo

**Descripción:** todo lo de un Equipo en su Liga, organizado en pestañas: Resumen, Partidos, Clasificación, Plantilla y Estadísticas. Al entrar, la app adopta el Tema del Equipo. Si el Equipo ha jugado varias fases, se muestra la actual y se puede elegir otra. Realiza UJ-1, UJ-2 y UJ-4.

#### FR-4: Resumen
El Seguidor ve el próximo Partido, el último resultado, la posición, los puntos, los Partidos jugados, los goles a favor y en contra, y la Racha. Realiza UJ-1.

**Consecuencias (testeables):**
- Los datos coinciden con los publicados por la FCF para ese Grupo.
- Un Partido pendiente de una Jornada anterior aparece como próximo Partido según su fecha. Si el próximo Partido está aplazado sin fecha, se muestra el siguiente programado y un aviso del aplazado.

#### FR-5: Partidos
El Seguidor ve todos los Partidos de Liga del Equipo en la fase, por Jornada: rival, casa o fuera, fecha, hora, campo y resultado. Realiza UJ-2.

**Consecuencias (testeables):**
- El orden es por Jornada; un aplazado se queda en su Jornada con la nueva fecha o "sin fecha".
- Las Jornadas en que el Equipo descansa se muestran como "descansa".
- Los Resultados de despacho muestran el resultado oficial con la marca "despacho" y, entre paréntesis, el resultado del campo.
- Al tocar un Partido jugado se abre su Ficha de partido. Al tocar uno no jugado se ve la fecha, la hora, el campo y la dirección.
- Las horas son las de Catalunya tal como las publica la FCF. Un Partido sin hora fijada se muestra "hora por confirmar".

#### FR-6: Clasificación
El Seguidor ve la clasificación del Grupo: posición, puntos, PJ, G, E, P, GF, GC, diferencia y Racha, con el Equipo destacado. Realiza UJ-1.

**Consecuencias (testeables):**
- Se marcan las posiciones de ascenso y descenso cuando la FCF las indica.
- Al tocar otro Equipo se abre su Ficha de equipo.
- Si la Competición no tiene clasificación (algunas categorías de base), la pestaña lo explica en lugar de aparecer vacía.

### 5.4 Ficha de partido

#### FR-7: Ver el Acta
El Seguidor ve, de un Partido jugado: resultado, fecha, campo, Jornada, árbitros, alineaciones (Titulares y Suplentes, con capitán y portero), goles con minuto y tipo (normal, penalti, en propia), tarjetas con minuto, cambios y cuerpo técnico. Realiza UJ-2.

**Consecuencias (testeables):**
- Sin Acta publicada se muestran los datos de programación y "acta pendiente de publicar". Con Acta sin cerrar, el resultado se marca "provisional".
- Si la FCF corrige el Acta, la Ficha muestra la versión nueva.
- Los goles sin minuto se muestran sin minuto.
- En Categorías de menores, Jugadores, técnicos y árbitros aparecen Anonimizados (FR-16).
- Al tocar un Jugador se abre su Ficha de jugador.

### 5.5 Plantilla y Jugadores

#### FR-8: Plantilla
El Seguidor ve la Plantilla del Equipo: dorsal más habitual, convocatorias, titularidades, goles, tarjetas amarillas y rojas, y una tabla por Jornada con Titular / Suplente / No convocado. Realiza UJ-2.

**Consecuencias (testeables):**
- Incluye a todos los Jugadores que han aparecido en alguna Acta del Equipo en la fase; se identifica a cada Jugador por su identificador de la FCF, no por el dorsal.
- Marca capitán y portero si el Acta los marca en algún Partido, y a los Debutantes.
- Se puede ordenar por cada columna. Por defecto, por titularidades.
- Los goles en propia puerta no suman al Jugador que los marca.

#### FR-9: Ficha de jugador
El Seguidor ve los totales de un Jugador en el Equipo en la Temporada (convocatorias, titularidades, goles, tarjetas, sanciones) y la lista de sus Partidos. Realiza UJ-2.

**Consecuencias (testeables):**
- Los totales coinciden con la suma de sus Actas.
- Un Jugador que juega en dos Equipos del mismo Club tiene una ficha en cada uno, con un enlace entre ellas, salvo si una es de Categoría de menores (FR-16).

### 5.6 Rankings del Grupo

#### FR-10: Goleadores, joc net y sanciones del Grupo
El Seguidor ve los rankings del Grupo tal como los publica la FCF: goleadores (con goles de penalti), clasificación de joc net (amarillas, dobles amarillas, rojas) y sanciones del comité por Jornada.

**Consecuencias (testeables):**
- Coinciden con los publicados por la FCF, aunque difieran de lo que la app calcula a partir de las Actas.
- En Categorías de menores no se muestran los textos de las sanciones, solo a quién afectan (Anonimizado) y cuántos Partidos.

### 5.7 Estadísticas avanzadas

**Descripción:** lo que hoy Luis calcula a mano, para cualquier Equipo, gratis y abierto a todos, en la pestaña Estadísticas de la Ficha de equipo. Se calcula solo con los Partidos válidos de la fase. Indica sobre cuántos Partidos válidos se calcula. Realiza UJ-3 como base del Dossier.

#### FR-11: Quién marca primero
El Seguidor ve en cuántos Partidos válidos marcó primero el Equipo y cuántos de esos ganó (p. ej. "marcó primero en 3 de 4, ganó 1").

**Consecuencias (testeables):**
- Un 0-0 cuenta en el total, no como "marcó primero".
- Si falta el minuto de algún gol, ese Partido no entra en el cálculo y se indica.

#### FR-12: Goles por Tramo
El Seguidor ve los goles a favor y en contra repartidos en 6 Tramos iguales de la duración del Partido.

**Consecuencias (testeables):**
- En un Partido de 90 minutos, los Tramos son 1-15, 16-30, 31-45, 46-60, 61-75 y 76-90. Los goles se reparten según el minuto que publica la FCF; un minuto mayor que la duración cuenta en el último Tramo.
- En Competiciones con Partidos más cortos, los Tramos se ajustan a su duración.
- Los goles sin minuto no entran en los Tramos, y se indica cuántos son.

#### FR-13: Once más repetido
El Seguidor ve los 11 Jugadores (7 en Futbol 7) con más titularidades, con dorsal, titularidades sobre Partidos válidos y goles.

**Consecuencias (testeables):**
- Los empates se deshacen por convocatorias y después por goles.

#### FR-14: Sanciones vigentes
El Seguidor ve qué Jugadores del Equipo tienen una sanción pendiente, cuántos Partidos les quedan y si pueden jugar el próximo Partido.

**Consecuencias (testeables):**
- Si no se puede deducir con certeza cuántos Partidos quedan, se muestra la sanción sin contador ni veredicto.

### 5.8 Protección de menores

**Descripción:** la FCF publica con nombre completo a niños y adolescentes. Wrapper FCF no amplifica esa exposición. Realiza UJ-4.

#### FR-15: Detectar Categorías de menores
La app clasifica cada Competición como de adultos o Categoría de menores.

**Consecuencias (testeables):**
- Juvenil, cadete, infantil, alevín, benjamín y prebenjamín (también femeninas) son Categorías de menores.
- Una Competición que no se puede clasificar con certeza se trata como Categoría de menores.
- El Administrador puede marcar una Competición como de adultos.

#### FR-16: Anonimizar en Categorías de menores
En las Categorías de menores, Jugadores, técnicos y árbitros aparecen Anonimizados en todas las pantallas, rankings, Notificaciones y Dossiers, para todos los roles, Gestores y Administrador incluidos.

**Consecuencias (testeables):**
- Nunca aparece un nombre completo de una persona en una Categoría de menores.
- No se muestran los textos de las sanciones del comité.
- La Ficha de jugador de un menor no se enlaza ni se fusiona con la de un Equipo de adultos, aunque sea la misma persona según la FCF.
- Las estadísticas se mantienen.

#### FR-17: Retirar un nombre a petición
El Administrador puede Anonimizar a un Jugador concreto de cualquier Competición si la persona lo pide.

### 5.9 Tema y Marca

#### FR-18: Tema automático
Cada Equipo tiene un Tema por defecto con su escudo y los colores de su primera equipación tal como los publica la FCF. Realiza UJ-4.

**Consecuencias (testeables):**
- Cualquier Equipo de la v1 tiene Tema sin intervención humana; si a la FCF le falta el dato, se usa un Tema neutro.
- El Tema nunca deja texto ilegible: si los colores no dan contraste suficiente, se ajustan.

#### FR-19: Marca manual (Hito 2)
El Gestor puede ajustar la Marca de su Equipo (o de todos los Equipos de su Club, si gestiona el Club): logo, dos colores y enlaces a redes. Se aplica para todos los Seguidores.

**Consecuencias (testeables):**
- Los colores que no dan contraste suficiente se rechazan con una explicación.
- El Administrador puede volver al Tema automático de cualquier Equipo.
- En el futuro requerirá Plan; en v1 es gratis.

**Fuera de alcance:** sacar la Marca de las redes sociales (post-MVP).

### 5.10 Cuentas, roles y Solicitudes de gestión (Hito 2)

#### FR-20: Cuenta opcional
Cualquier usuario puede crear una Cuenta para sincronizar Equipos seguidos (FR-2), recibir Notificaciones y enviar Solicitudes de gestión.

#### FR-21: Solicitud de gestión
Un usuario con Cuenta puede pedir ser Gestor de un Equipo o de un Club entero, indicando su relación con él. Realiza UJ-3 y UJ-5.

**Consecuencias (testeables):**
- Si el Equipo o Club no tiene Gestores, la Solicitud la decide el Administrador. Si ya tiene, la deciden sus Gestores.
- Quien la pidió ve su estado (pendiente, aprobada, rechazada) y recibe una Notificación cuando cambia.
- Un Gestor de un Club es Gestor de todos sus Equipos.
- Un Equipo puede tener varios Gestores.

#### FR-22: Retirar a un Gestor
El Administrador, o otro Gestor del mismo Equipo o Club, puede retirar a un Gestor.

**Consecuencias (testeables):**
- Quien deja de ser Gestor pierde al momento el acceso a los Dossiers de ese Equipo.
- Los Dossiers que pidió siguen disponibles para los demás Gestores.

#### FR-23: Preparado para Planes
Los permisos de Dossier, Marca manual y Claves se asignan a un Equipo o a un Club, no a una persona, para que en el futuro un Plan de pago por Equipo o por Club los desbloquee sin rehacer nada. En v1 no hay pago y todo Gestor tiene esas funciones.

### 5.11 Dossier (Hito 2)

**Descripción:** el dossier que hoy Luis hace a mano, generado por la app para un rival concreto. Respecto a las Estadísticas avanzadas públicas, aporta: todo en una vista, comparado con el propio Equipo, con la lista de próximos rivales, y privado para el cuerpo técnico. `[NOTA PM]` Las Estadísticas avanzadas del propio Equipo también son públicas, así que el rival puede verlas en su Ficha de equipo; lo privado es el trabajo de preparación del Gestor. Realiza UJ-3.

#### FR-24: Próximos rivales y pedir un Dossier
El Gestor ve la lista de los próximos Partidos de Liga de su Equipo y puede pedir el Dossier del rival de cualquiera de ellos.

**Consecuencias (testeables):**
- El Dossier está listo en menos de 5 minutos.
- Si el rival no tiene Partidos válidos, el Dossier lo dice en lugar de mostrar estadísticas vacías.
- Si varios Gestores piden el mismo Dossier, existe uno solo.

#### FR-25: Contenido del Dossier
El Dossier incluye, del rival: posición, puntos, goles, Racha; resultados por Jornada (casa o fuera, aplazados, Resultados de despacho); quién marca primero; goles por Tramo; once más repetido; Plantilla con tabla por Jornada; sus goleadores; totales de tarjetas (amarillas, dobles amarillas, rojas); sanciones vigentes; Debutantes del último Partido; y el Partido en cuestión (fecha, hora, campo, casa o fuera). Incluye también **Nuestra ficha** (los mismos bloques del propio Equipo) y la clasificación del Grupo con los dos Equipos destacados.

**Fuera de alcance:** Claves y frases-resumen narrativas (post-MVP, con IA).

#### FR-26: Un Dossier vivo hasta el Partido
El Dossier se actualiza solo con los nuevos datos de la FCF hasta el inicio del Partido, y después queda fijo.

**Consecuencias (testeables):**
- Muestra "Datos FCF a <fecha y hora>".
- Si el Partido se aplaza, el Dossier sigue vivo hasta la nueva fecha.

#### FR-27: Acceso y enlace del Dossier
Solo los Gestores del Equipo que lo pidió ven el Dossier. El Gestor puede copiar su enlace para compartirlo.

**Consecuencias (testeables):**
- El enlace pide iniciar sesión y solo abre con la Cuenta de un Gestor de ese Equipo (o de su Club).
- Un Seguidor, un Gestor de otro Equipo o un visitante sin Cuenta no pueden abrirlo.
- Los Dossiers son del Equipo: sobreviven a la retirada de quien los pidió (FR-22).

### 5.12 Notificaciones (Hito 2)

**Descripción:** avisos para usuarios con Cuenta sobre sus Equipos seguidos. En iPhone requieren tener la app instalada.

#### FR-28: Tipos de Notificación
El usuario con Cuenta recibe Notificaciones de:
- resultado publicado de un Partido de un Equipo seguido;
- resultado modificado (la FCF corrige un resultado ya avisado);
- cambio de fecha, hora o campo de un próximo Partido, o aplazamiento;
- recordatorio de Partido con hora y campo, el mismo día 3 horas antes;
- sanción del comité a un Jugador de un Equipo seguido;
- cambio de estado de su Solicitud de gestión.

**Consecuencias (testeables):**
- Se puede activar o desactivar cada tipo para cada Equipo seguido. Por defecto, todos activos.
- Al seguir un Equipo no llegan Notificaciones de lo ya ocurrido.
- Un Partido entre dos Equipos seguidos genera una sola Notificación de cada tipo.
- No se envía dos veces la misma Notificación.
- En Categorías de menores, las personas aparecen Anonimizadas.

### 5.13 Idioma, frescura, fuente y medición

#### FR-29: Catalán y castellano
La interfaz está en catalán y en castellano. Por defecto, el idioma del dispositivo si es uno de los dos, y si no, catalán; se cambia en los ajustes. Los datos de la FCF se muestran tal como vienen, sin traducir.

#### FR-30: Frescura de los datos
Un resultado, un Acta, un cambio de Partido o una sanción publicados por la FCF aparecen en la app en una hora como máximo.

#### FR-31: Si la FCF no responde
Si la API de la FCF cae o cambia, la app sigue mostrando los últimos datos buenos con "actualizado hace X". Si pasan más de 3 horas sin datos nuevos, muestra un aviso de que la FCF no responde. Nunca muestra un dato dudoso en lugar de uno viejo.

#### FR-32: Atribución
La app indica que los datos proceden de la FCF y que no es una app oficial de la FCF.

#### FR-33: Medición de uso
El Administrador ve, por Equipo, cuántos Seguidores tiene (con y sin Cuenta) y cuántos usuarios lo han abierto cada semana, y cuántos Dossiers se piden. Sirve para medir §8.

## 6. Non-Goals (explícitos)

- No hay resultados en directo: la app muestra lo que publica la FCF, cuando lo publica.
- No es una app oficial de la FCF ni lo aparenta.
- No hay contenido de usuarios: ni fotos, ni crónicas, ni convocatorias propias.
- No gestiona el club: ni fichas, ni cuotas, ni entrenamientos.
- No hay apuestas ni chat.
- No hay copas, torneos, promociones ni fases de ascenso: solo la Liga.
- No hay pago en v1.
- No es una app nativa de tiendas: es una PWA.
- No muestra los datos de contacto de los clubs ni sus horarios de entrenamiento, aunque la FCF los publique.

## 7. Alcance del MVP

### 7.1 Dentro

**Primera entrega (23/10/2026), solo para el Guinardó A:**
- La app abre directamente en la Ficha de equipo del Guinardó A, sin búsqueda ni Feed.
- FR-4 (Resumen), FR-5 (Partidos), FR-6 (Clasificación), FR-7 (Ficha de partido) y FR-8 (Plantilla), completos.
- FR-18 (Tema automático), FR-30 (frescura) y FR-32 (atribución).
- En catalán y castellano (FR-29), con catalán por defecto.
- Publicada en una dirección web que Luis pueda compartir con el club.

**Hito 1, "el Guinardó la usa"** (sin Cuentas): FR-1, FR-2 (sin sincronización), FR-3 a FR-18, FR-29 a FR-32, y la parte de FR-33 que no necesita Cuentas.

**Hito 2, "listo para otros clubs":** FR-19 a FR-28, la sincronización de FR-2 y FR-33 completo.

### 7.2 Fuera del MVP

- **Pasarela de pago y Planes:** v1 gratis; los permisos ya están preparados (FR-23).
- **Claves escritas por IA:** aplazadas por Luis. `[NOTA PM]` Es lo más valioso del dossier manual y lo primero que conviene hacer tras el MVP.
- **Marca desde redes sociales:** frágil (bloqueos, condiciones de uso de Instagram y X) y la FCF no da las cuentas de cada club.
- **Copas y fases de ascenso.**
- **Futbol 5, Futbol Sala, Futbol Sala Femení, Futbol Platja.**
- **Mapa del campo y compartir como imagen:** descartados para v1.
- **Temporadas anteriores:** solo se muestra la Temporada acabada durante el verano.

## 8. Métricas de éxito

- **SM-1:** el cuerpo técnico del Guinardó A usa la app cada semana en lugar de fcf.cat (desde el Hito 1) y del dossier manual (desde el Hito 2). Objetivo: 4 Jornadas seguidas. Se mide con FR-33. Valida FR-4 a FR-14 y FR-24 a FR-27.
- **SM-2:** 20 Seguidores del Guinardó A en el primer mes tras el Hito 1. Se mide con FR-33. Valida FR-1 a FR-3.
- **SM-3:** preparar un rival pasa de horas a menos de 10 minutos. Valida FR-24 y FR-25.
- **Counter-metric SM-4:** ninguna discrepancia entre la app y la FCF en resultados, clasificación y Actas que no se explique por FR-30 (retraso) o FR-31 (FCF caída). Valida FR-30 y FR-31.

## 9. Preguntas abiertas

1. ¿Permite la FCF reutilizar sus datos? Q-1 en `client-questions.md`.
2. ¿Está de acuerdo el Guinardó con mostrar datos de sus equipos base, aunque estén Anonimizados? Q-2 en `client-questions.md`.
3. (Interna, para la spec) Duración de los Partidos por Competición para los Tramos (FR-12): normativa de la FCF o minutos de las Actas.
4. (Interna, para la spec) Cómo distinguir una Liga de una copa o una promoción a partir de los datos de la FCF.
5. (Interna, para la spec) Códigos de tipo de gol y de tarjeta que aún no se han visto (penalti, en propia, doble amarilla, roja), y el estado `ESTADO=3` de algunos Partidos.
6. (Interna) Con qué retraso publica la FCF el resultado tras el Partido. Afecta a lo que el usuario puede esperar en UJ-2.

## 10. Índice de Assumptions

*Todas confirmadas por Luis al finalizar el PRD (22/10/2026); A-10 cambiada a petición suya. Ya no quedan `[ASSUMPTION]` abiertas en el documento.*

| # | Dónde | Decisión | Confirmada por |
|---|---|---|---|
| A-1 | §2 | Tipo de proyecto: MVP de validación con el propio club, abierto a todos | Luis |
| A-2 | FR-2 | Un Equipo seguido aparece en el Feed en menos de 1 minuto | Luis |
| A-3 | FR-2 | Sin límite de Equipos seguidos | Luis |
| A-4 | FR-14 | Sin certeza sobre una sanción, se muestra sin contador ni veredicto | Luis |
| A-5 | FR-17 | El Administrador puede Anonimizar a un Jugador concreto a petición | Luis |
| A-6 | FR-24 | El Dossier está listo en menos de 5 minutos | Luis |
| A-7 | FR-28 | Recordatorio el mismo día, 3 horas antes | Luis |
| A-8 | FR-29 | Idioma por defecto: el del dispositivo; si no es ca ni es, catalán | Luis |
| A-9 | FR-31 | Aviso de FCF caída tras 3 horas sin datos | Luis |
| A-10 | §7.1 | La Primera entrega es bilingüe, con catalán por defecto | Luis |
| A-11 | SM-1, SM-3 | Cifras: 4 Jornadas seguidas; menos de 10 minutos | Luis |
