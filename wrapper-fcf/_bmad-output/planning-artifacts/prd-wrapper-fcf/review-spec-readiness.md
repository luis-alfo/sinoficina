---
title: Revisión de preparación para spec — PRD Wrapper FCF
reviewed: prd.md (draft, 2026-10-22)
contrasted_with: .decision-log.md, fcf/ENDPOINTS.md
date: 2026-10-22
---

# Revisión de preparación para spec (spec-readiness)

**Veredicto:** NO listo para `nch-spec` en bloque. Las features 5.4, 5.6 y 5.13 están casi listas; 5.1, 5.2, 5.8 y 5.11 bloquean. Hay 2 hallazgos críticos (qué es exactamente un Equipo y de dónde sale la lista de Equipos de un Club) que afectan a todo el Hito 1, y 8 altos que obligarían a la spec a volver a preguntar decisiones de producto.

Recuento: 2 críticos · 8 altos · 17 medios · 9 bajos.

Convención: "Arreglo" = decisión de producto que hay que tomar o texto que hay que añadir al PRD. "API" = endpoint consultado en `fcf/ENDPOINTS.md`.

---

## Críticos

### C-1 · FR-1 / 5.1 — Listar "los Equipos de un Club" no está soportado por ningún endpoint documentado
- **Problema:** FR-1 promete "al elegir un Club se listan sus Equipos de la Temporada en curso… con su Competición y Grupo de liga". API: `/search?q=` devuelve clubs, camps, news, competicions (no Equipos ni la relación Club→Equipos); `/clubs/{clubId}/team/{equipId}` exige conocer ya el `equipId`; `/competition/equipos?grupId=` va por Grupo. La única vía documentada es recorrer `temporadas → disciplines → competicions → grupos → equipos` para las 3 Disciplinas y construir un índice propio. Además no consta que `/search` ignore acentos ("guinardo" → "GUINARDÓ, C.F."). Es el corazón del self-service de UJ-1.
- **Arreglo:** (a) verificar si existe un endpoint Club→Equipos (p. ej. `/clubs/{clubId}`) y documentarlo en ENDPOINTS.md; si no, (b) añadir a 5.1 la capacidad explícita: "La app mantiene un catálogo de todos los Equipos de las Disciplinas v1 de la Temporada en curso, obtenido recorriendo todos los Grupos; se refresca cada N horas/días; un Equipo nuevo aparece en la búsqueda como máximo N después de publicarse". La búsqueda accent-insensitive se hace contra ese catálogo, no contra `/search`.

### C-2 · §4 Glosario (Equipo, Competición) / FR-1, FR-2, FR-4 — "liga" no está definida y la identidad del Equipo es inestable
- **Problema:** Equipo = "conjunto inscrito en **una** Competición de **una** Temporada", pero FR-1 muestra Equipos "con su Competición y Grupo **de liga**" (implica varias Competiciones por Equipo). "Liga" es el concepto que filtra todo (§4 Competición, §6, 5.5, 5.7) y no está definido ni hay regla para distinguir liga de copa en `/competition/competicions` (solo `value`/label). Sin regla: (1) qué entrada se sigue; (2) qué pasa en fútbol base si la liga cambia de Grupo a mitad de Temporada (fases); (3) qué pasa con los Equipos seguidos al cambiar de Temporada ("Temporada en curso" tampoco tiene regla de cambio, `/competition/temporadas` solo lista).
- **Arreglo:** añadir al glosario **Liga** ("Competición de formato todos contra todos de un Equipo en la Temporada; se identifica por …[regla sobre el nombre/tipo de Competición]") y redefinir Equipo como la inscripción de un Club en una Disciplina/categoría que se sigue entre Temporadas y Grupos. Decidir: "Si la liga del Equipo cambia de Grupo (nueva fase), el seguimiento pasa al Grupo nuevo y las estadísticas [suman / se reinician]". "La Temporada en curso cambia cuando la FCF publica el calendario de la nueva (fecha X); los Equipos seguidos [se migran automáticamente si el mismo Club tiene un Equipo equivalente / se avisa al usuario]".

---

## Altos

### H-1 · FR-26 vs FR-27 (A-5) vs decision log — Visibilidad del Dossier contradictoria
- **Problema:** FR-26: "Solo los Gestores… Ningún Seguidor". Glosario: Enlace privado "solo abre quien la recibe" (no verificable). A-5: "se abre sin Cuenta". Decision log (l.22, l.27): "Solo lo ve el Gestor / quien gestiona". Con A-5, cualquiera que reciba el enlace reenviado (incluido el rival) lo abre.
- **Arreglo:** decidir una de dos y reescribir FR-26 y el glosario en coherencia: (a) "El Dossier lo ven los Gestores del Equipo y cualquiera que abra un Enlace privado vigente; el Gestor asume que el enlace es reenviable" o (b) "El Enlace privado exige Cuenta y el Gestor da acceso a Cuentas concretas". Añadir: caducidad exacta ("al terminar el Partido" = hora de inicio + duración, o al publicarse el Acta), si el Gestor puede generar varios enlaces y si al revocar el rol de Gestor (FR-22) se revocan sus enlaces.

### H-2 · FR-17 vs FR-12 / FR-31 / FR-32 — Los textos de sanciones llevan nombres completos de menores
- **Problema:** API `/competition/sanciones` devuelve "texto del comité" libre con nombres. FR-32 dice que esos textos "se muestran tal como vienen"; FR-17 exige anonimizar en "todas las pantallas, rankings, notificaciones y Dossiers". Incompatibles para Categorías de menores. Lo mismo para `/goleadores` y `/joc-net` (campos no documentados).
- **Arreglo:** añadir a FR-17: "En Categorías de menores no se muestra el texto original de la sanción; se muestra [Jugador Anonimizado + nº de Partidos + motivo si se puede extraer / solo 'sanción de N partidos']". Ajustar FR-32: "…sin traducir, salvo la anonimización de FR-17". Decidir si cuerpo técnico y árbitros (adultos) aparecen con nombre completo también en Categorías de menores.

### H-3 · FR-17 / §4 Anonimizado / §9-4 — Formato de anonimización inconsistente y detección de menores delegada a la spec
- **Problema:** glosario: "D. A. #8" (2 iniciales + dorsal); FR-17: "Q. A. V. o similar" (3 iniciales, sin dorsal). "o similar" no es testable. El dorsal cambia entre Actas. La lista de qué Competiciones son de menores (pregunta 9-4) es una decisión de producto (¿juvenil incluido? ¿femení base?), no técnica.
- **Arreglo:** fijar el formato exacto, p. ej. "Inicial del nombre + inicial del primer apellido + dorsal más frecuente en la Temporada: 'Q. A. #8'", y la regla de desempate si dos Jugadores coinciden. Sustituir 9-4 por la regla: "Es Categoría de menores toda Competición cuyo nombre contiene: Juvenil, Cadet, Infantil, Aleví, Benjamí, Prebenjamí, Debutant… (lista cerrada)". Con A-3: decidir si un Enlace privado abierto sin Cuenta muestra nombres o Anonimizados.

### H-4 · FR-3, FR-5, FR-25, glosario (Partido, Resultado de despacho) — Aplazado y despacho no constan en la API
- **Problema:** API `/competition/partidos` documenta `CODACTA`, equipos, escudos, resultado, campo, lat/long; `/competition/acta` documenta `CERRADA`/`ESTADO` y `GOLES_*`. No hay campo de estado "aplazado", ni marca de despacho, ni "resultado en el campo" (FR-5: "3-0*, en el campo 0-1"). Tampoco se decide si un Resultado de despacho cuenta en racha, quién marca primero, goles por Tramo, once más repetido.
- **Arreglo:** verificar y documentar los campos en ENDPOINTS.md. Si no existen, decidir regla: "Aplazado = Partido con fecha pasada sin resultado y sin Acta [o con campo X]"; "Despacho: si no es detectable, no se marca" o "se deduce de `/sanciones`". Añadir: "Los Resultados de despacho cuentan para clasificación y racha (como la FCF) y NO cuentan para FR-13/FR-14/FR-15 (se usan los eventos del Acta del campo)" — o la decisión contraria.

### H-5 · FR-3 / 5.2 — Orden y ventana del Feed sin decidir
- **Problema:** "orden cronológico" sin sentido (¿ascendente? ¿próximos arriba y resultados abajo?), "como mínimo" próximo + último sin máximo, sin ventana temporal, sin agrupación. Sin regla para: fin de Temporada (sin próximo Partido), Partido entre dos Equipos seguidos (¿qué Tema lleva la tarjeta? ¿sale una o dos veces?), tocar una tarjeta.
- **Arreglo:** p. ej. "El Feed agrupa por día; arriba los Partidos de hoy, luego próximos en orden ascendente (hasta 7 días), luego resultados de los últimos 7 días en orden descendente. Mínimo: próximo y último de cada Equipo aunque caigan fuera. Un Partido entre dos Equipos seguidos sale una vez, con el Tema del Equipo local. Tocar una tarjeta abre la Ficha de partido."

### H-6 · FR-14 / §9-3 — Tramos no deducibles con los datos del Acta
- **Problema:** API: los goles traen solo `minuto`, sin parte ni añadido. Un gol en el 47' puede ser 45+2 (1.ª parte) o 47 (2.ª); la regla "el añadido cuenta en el último Tramo de su parte" no es aplicable ni testable. La duración por categoría (§9-3) se delega a la spec, pero es un dato de producto; y en duraciones no divisibles entre 6 (p. ej. 2×25') falta regla de redondeo de fronteras.
- **Arreglo:** decidir: "Un minuto > duración de la 1.ª parte y ≤ duración 1.ª parte + 5 se asigna a [Tramo 3 / Tramo 4]" (o aceptar el sesgo y decirlo). Incluir en el PRD la tabla de duración por categoría (Amateur 90, Juvenil 90, Cadet 80, Infantil 70, Aleví F7 50, Benjamí F7 50…, a validar con la normativa FCF) y la regla: "fronteras = duración × k/6, redondeo hacia arriba; minuto 0 cuenta en el Tramo 1". Decidir qué se hace con goles sin minuto y en propia puerta (¿a favor de quién?).

### H-7 · FR-24 / FR-25 / FR-27 — Ciclo de vida del Dossier sin definir
- **Problema:** "disponible en minutos" no es testable (SM-3 dice < 10 min de preparación). No se decide si el Dossier es una foto fija al pedirlo o se actualiza con nuevas Actas; si se guarda y dónde se listan los anteriores; si se puede volver a pedir; si se puede pedir para Partidos ya jugados ("cualquier Partido de liga"). FR-25 "el próximo Partido (fecha, hora, campo, casa o fuera)" es ambiguo: ¿el Partido entre ambos o el próximo del rival?
- **Arreglo:** p. ej. "El Dossier se genera en menos de 2 minutos; es una foto fija con fecha de generación visible; el Gestor puede regenerarlo; los Dossiers se listan en la Ficha del Partido y en 'Mis Dossiers'; solo para Partidos no jugados". FR-25: "el Partido para el que se pidió (fecha, hora, campo, si el rival juega en casa o fuera)".

### H-8 · FR-33 / §2 / SM-4 — Comportamiento cuando la FCF falla o cambia
- **Problema:** §2 reconoce que la API "puede cambiar sin aviso" y SM-4 exige cero discrepancias, pero el PRD no dice qué ve el usuario si los datos no se pueden actualizar (API caída, 500 `Failed to fetch competition data`, cambio de formato). No hay forma de que el usuario sepa si lo que ve está al día.
- **Arreglo:** añadir consecuencias a FR-33: "Cada pantalla de datos indica 'Actualizado hace X'. Si la última actualización correcta tiene más de 2 h, se muestra un aviso 'Datos de la FCF no disponibles temporalmente'. Nunca se muestra un dato a medias: o la versión anterior completa o la nueva." Y: "El Administrador recibe un aviso si la sincronización falla N veces seguidas".

---

## Medios

### M-1 · FR-1 — Búsqueda por Equipo, orden y casos borde
- El enunciado dice "Club o Equipo" pero las consecuencias solo cubren Clubs. Falta: ¿se busca por nombre de Equipo ("Guinardó A")? orden de resultados; qué pasa con < 3 caracteres; Club sin Equipos en Disciplinas v1 (solo sala); orden de la lista de Equipos de un Club.
- **Arreglo:** "Solo se buscan Clubs. Resultados por coincidencia exacta primero y luego alfabético, máx. 20. Con < 3 caracteres no se busca. Equipos del Club ordenados por Disciplina y categoría (de mayor a menor edad), y dentro por letra. Club sin Equipos v1: 'Este Club no tiene Equipos de Futbol 11, Futbol 7 ni Futbol Femení'."

### M-2 · 5.1 — "funcionan de inmediato" no es testable
- Al seguir un Equipo hay que traer todas las Actas del Grupo/Equipo (API: una llamada a `/acta` por Partido).
- **Arreglo:** "El resumen y calendario aparecen en < 5 s; plantilla y Estadísticas avanzadas en < N s; mientras, se muestra un indicador de carga, nunca cifras parciales."

### M-3 · FR-2 — Fusión con Cuenta existente y cierre de sesión
- Solo cubre "al crear la Cuenta". Falta: iniciar sesión en una Cuenta existente desde un dispositivo con seguidos locales; cerrar sesión.
- **Arreglo:** "Al iniciar sesión se unen los seguidos locales y los de la Cuenta. Al cerrar sesión, el dispositivo conserva [ninguno / los de la Cuenta]."

### M-4 · FR-4 — Próximo Partido aplazado sin nueva fecha, y racha
- **Arreglo:** "Un Partido aplazado sin fecha no cuenta como próximo; se muestra aparte como 'aplazado, sin fecha'. Racha = últimos 5 Partidos jugados por fecha, incluye Resultados de despacho." Indicar qué se muestra si no hay próximo Partido (fin de Temporada).

### M-5 · 5.3 — Estructura de la Ficha de equipo sin cerrar
- 5.3 dice "resumen, calendario y resultados, clasificación", pero 5.5 (plantilla), 5.7 ("en su Ficha de equipo") y 5.6 (Rankings, sin punto de entrada) también cuelgan de algún sitio.
- **Arreglo:** listar las secciones de la Ficha de equipo (p. ej. Resumen · Partidos · Clasificación · Plantilla · Estadísticas · Rankings del Grupo) y desde dónde se llega a la Ficha de jugador y a los Rankings.

### M-6 · FR-5 / FR-7 — Tocar Partidos no jugados y jornadas de descanso
- FR-5 solo abre Ficha de partido si está jugado; FR-7 describe una Ficha para Partidos sin Acta. Grupos impares: Jornada en que el Equipo descansa.
- **Arreglo:** "Todo Partido abre su Ficha de partido; sin Acta muestra programación. En Jornadas sin Partido se muestra 'descansa'."

### M-7 · FR-7 / glosario Partido — Estados del Partido incompletos; Acta no cerrada
- Estados: programado, aplazado, jugado. Faltan "jugado sin Acta publicada", "suspendido". "Pendiente" se usa con tres sentidos (FR-4, FR-5, FR-7). API: `CERRADA`/`ESTADO` = 1 cerrada; ¿se muestra un Acta abierta?
- **Arreglo:** definir en §4 los estados (Programado, Aplazado, Suspendido, Jugado-sin-Acta, Con Acta) y "Solo se muestra y se usa para estadísticas un Acta con `CERRADA = 1`" (coherente con §6 sin directo).

### M-8 · FR-7 / FR-10 / FR-11 — Códigos de gol y tarjeta no observados
- API `/acta`: solo se han visto `tipo_gol = 100` y `tipo_tarjeta = 100`; penalti, propia, doble amarilla y roja sin código. FR-10 pide "goles de penalti" y `/goleadores` no documenta campos; `/joc-net` tampoco (FR-11).
- **Arreglo:** decidir el comportamiento con código desconocido ("se muestra como gol/tarjeta sin tipo") y que goles de penalti en FR-10 se omiten si `/goleadores` no los da. Completar ENDPOINTS.md con los campos de `/goleadores`, `/joc-net`, `/classificacio` (¿racha?, ¿`promociones` = ascenso/descenso de FR-6?) y `sustituciones` (¿minuto, entra/sale?).

### M-9 · FR-8 / FR-15 — Dorsal, capitán y portero a nivel de plantilla; desempates
- Dorsal, capitán y portero son por Acta. ¿Qué dorsal se muestra en la plantilla? ¿"capitán" = alguna vez o la mayoría? FR-15: desempate en titularidades; ¿Futbol Femení usa 11 o 7? (es una Disciplina con F11 y F7). Orden por defecto de FR-8.
- **Arreglo:** "Dorsal = el más frecuente (empate: el último). Capitán/portero = lo fue en ≥ 1 Partido, con contador. Once: desempate por minutos/convocatorias/goles. Tamaño 7 u 11 según el formato de la Competición. Orden por defecto: titularidades desc."

### M-10 · FR-8 / §4 — "Debutante" no definido
- Aparece en FR-8, en el glosario de Estadísticas avanzadas, en UJ-3 y FR-25, sin definición: ¿primera convocatoria o primera titularidad/minutos? ¿"último Partido" del Equipo?
- **Arreglo:** añadir a §4: "**Debutante** — Jugador cuya primera convocatoria de la Temporada con ese Equipo es el último Partido con Acta del Equipo."

### M-11 · FR-9 / §4 Jugador — Jugador que juega en varios Equipos
- En base y amateur es habitual que un Jugador del B sea convocado con el A. Glosario: Jugador "aparece en Actas de **un** Equipo". API `/jugador-stats?codgrupo=` es por Grupo. No se decide si la Ficha de jugador es por Equipo o agrega todos sus Equipos.
- **Arreglo:** "La Ficha de jugador muestra totales por Equipo (una sección por Equipo en que aparece) y un total global." o "solo del Equipo desde el que se abrió".

### M-12 · FR-13 — Denominador de "quién marca primero"
- **Arreglo:** "Sobre Partidos con Acta y con ≥ 1 gol: nº en que marcó primero el Equipo y resultado (G/E/P) de esos; también nº en que marcó primero el rival y su resultado. Los 0-0 se cuentan aparte."

### M-13 · FR-18 — Qué colores, qué formato, fallback y criterio de legibilidad
- API `/competition/equipacions`: camiseta, pantalón, medias, principal y alternativa; filas duplicadas (decision log l.17). No se decide qué prendas forman el Tema, ni qué pasa si un Equipo no tiene color. "Nunca deja texto ilegible" no es medible.
- **Arreglo:** "Color primario = camiseta principal; secundario = pantalón principal (si es igual, medias). Sin datos: Tema neutro de la app. Todo texto cumple contraste WCAG AA 4.5:1; si el color no lo cumple se oscurece/aclara hasta cumplirlo."

### M-14 · FR-19 — Marca manual sin consecuencias testeables
- Falta: formatos y tamaño del logo; qué redes; si el logo sustituye al escudo también en tarjetas del Feed y en la clasificación de otros; validación de contraste (¿aplica FR-18?); volver al Tema automático; varios Gestores editando; moderación (el Administrador "modera", §3.1).
- **Arreglo:** añadir consecuencias: "Logo PNG/SVG ≤ 1 MB; redes: Instagram, X, TikTok, web; el logo sustituye al escudo en toda la app; se aplica la regla de contraste de FR-18; botón 'restaurar Tema FCF'; el último cambio gana; el Administrador puede retirar una Marca."

### M-15 · FR-20 / FR-21 / FR-22 — Cuentas y Solicitudes sin consecuencias suficientes
- FR-20 no tiene consecuencias: método de alta (email + enlace mágico, Google…), borrado de Cuenta, edad mínima (los usuarios pueden ser los propios menores). FR-21: "relación" ¿texto libre u opciones?; repetir tras rechazo; duplicadas; canal del "aviso" (push requiere PWA instalada en iPhone). FR-22: cómo se entera el Administrador (UJ-5 "recibe"); efecto de retirar el rol (Dossiers, Enlaces, Marca).
- **Arreglo:** decidir cada punto y añadirlo como consecuencias; p. ej. "Alta por email con enlace mágico; la Cuenta se puede borrar y con ella sus datos. Relación: Entrenador / Delegado / Junta / Jugador / Familia / Otro + texto. Una sola Solicitud pendiente por Equipo. Aviso por email. El Administrador recibe email por Solicitud. Al retirar el rol se revocan sus Enlaces privados; sus Dossiers siguen visibles para los demás Gestores."

### M-16 · FR-28–FR-31 — Detalles de notificaciones
- Falta: estado por defecto de cada tipo al seguir un Equipo; FR-28 ¿un aviso por resultado y otro por Acta, o uno solo? ¿se avisa de correcciones posteriores?; FR-29 "próximo Partido" ¿solo el siguiente o cualquiera futuro?; FR-31 ¿incluye sanciones al cuerpo técnico? La API `/sanciones` da texto libre: no consta id de Jugador para atribuir la sanción a un Equipo seguido. Idioma del aviso (FR-32).
- **Arreglo:** "Todos activados por defecto. Un único aviso por Partido al publicarse el resultado; las correcciones no avisan. FR-29 cubre los Partidos de los próximos 14 días. FR-31 solo Jugadores, atribuidos por nombre+Equipo del texto; si no se puede atribuir, no se avisa. El aviso usa el idioma elegido en la Cuenta."

### M-17 · §7.1 Primera entrega / SM-2 — Decisiones que la spec tendría que volver a preguntar
- Primera entrega: no dice si incluye Feed/búsqueda (o el Guinardó A va fijo), Tema, ca/es, Ficha de jugador, atribución (FR-34). SM-2 ("20 Seguidores siguen el Equipo") no se puede medir en Hito 1 sin Cuentas: los seguidos viven en el dispositivo y el PRD no prevé analítica.
- **Arreglo:** listar FR exactos de la primera entrega (p. ej. FR-4, FR-5, FR-6, FR-7, FR-8, FR-18, FR-34; sin búsqueda, Equipo fijo, solo catalán). Añadir capacidad: "La app registra de forma anónima los altas/bajas de seguimiento por Equipo para medir SM-2" (y SM-1/SM-3: registro de Dossiers pedidos y tiempo hasta disponerlo).

---

## Bajos

- **L-1 · §4 — Términos clave usados y no definidos:** Ficha de equipo / de partido / de jugador, Plantilla, Racha, Aviso/Notificación (se usan como sinónimos: §5.12 "Notificaciones", FR-28 "Aviso", FR-21 "recibe aviso"), cuerpo técnico (Acta: "técnicos"). **Arreglo:** añadirlos a §4 y usar un solo término (p. ej. "Notificación").
- **L-2 · §4 Marca vs FR-19 — "escudo" vs "logo":** el Tema usa escudo; la Marca, logo. **Arreglo:** "Marca — … logo que sustituye al escudo".
- **L-3 · §4 Estadísticas avanzadas vs 5.7:** el glosario incluye "debutantes"; 5.7 no tiene FR de debutantes (están en FR-8). **Arreglo:** alinear la lista del glosario con FR-13–FR-16 o mover debutantes a 5.7.
- **L-4 · FR-14 — "categorías" en minúscula** sin definir (solo existe "Categoría de menores", definida como Competición). **Arreglo:** decir "Competiciones con Partidos más cortos".
- **L-5 · FR-23 — No testable:** es una restricción de diseño, no una capacidad. **Arreglo:** moverla a §2 o dejar una consecuencia verificable: "Los permisos se asignan por (Cuenta, Equipo o Club, rol); en v1 ninguna pantalla muestra precios ni Planes".
- **L-6 · FR-32 — Idioma por defecto y dónde se cambia:** **Arreglo:** "Por defecto, el idioma del dispositivo si es ca o es; si no, catalán. Se cambia en Ajustes; sin Cuenta se guarda en el dispositivo."
- **L-7 · FR-34 — Dónde se muestra la atribución:** **Arreglo:** "En el pie de cada pantalla de datos y en 'Acerca de'; la Ficha de partido enlaza al Acta original en fcf.cat."
- **L-8 · §8 SM-4 "Valida FR-33":** una métrica de exactitud valida FR-4/5/6/7 ("coinciden con la FCF"), no la frescura. **Arreglo:** corregir la referencia.
- **L-9 · Decision log vs PRD:** (a) l.13 marca el tipo de proyecto "inferido, a confirmar" y no hay confirmación posterior; el PRD lo da por cerrado. (b) l.47 fija la frescura de 1 h para "resultado o acta"; FR-33 la extiende a cambios de Partido y sanciones sin entrada en el log. (c) l.14 dice que en el futuro puede pagar "un seguidor"; el PRD (§1, §3.1, FR-23) solo contempla al Gestor. **Arreglo:** añadir al log la confirmación de Luis o ajustar el PRD.

---

## Estado por feature

| Feature | Estado | Bloqueado por |
|---|---|---|
| 5.1 Búsqueda y seguimiento | Bloqueada | C-1, C-2, M-1, M-2, M-3 |
| 5.2 Feed | Bloqueada | H-5, H-4 |
| 5.3 Ficha de equipo | Necesita decisiones | C-2, H-4, M-4, M-5, M-6 |
| 5.4 Ficha de partido | Casi lista | M-7, M-8 |
| 5.5 Plantilla y Jugadores | Necesita decisiones | M-9, M-10, M-11 |
| 5.6 Rankings del Grupo | Casi lista | H-2, M-8 |
| 5.7 Estadísticas avanzadas | Necesita decisiones | H-6, H-4, M-12 |
| 5.8 Categorías de menores | Bloqueada | H-2, H-3 |
| 5.9 Tema y Marca | Necesita decisiones | M-13, M-14 |
| 5.10 Cuentas y Solicitudes | Necesita decisiones | M-15, L-5 |
| 5.11 Dossier | Bloqueada | H-1, H-7 |
| 5.12 Notificaciones | Necesita decisiones | M-16 |
| 5.13 Idioma, frescura y fuente | Casi lista | H-8, L-6, L-7 |
