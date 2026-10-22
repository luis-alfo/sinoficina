---
title: 'Revisión de casos límite: PRD Wrapper FCF'
reviewer: edge-case hunter
date: 2026-10-22
scope: prd.md (FR-1..FR-34, UJ-1..UJ-5), .decision-log.md, fcf/ENDPOINTS.md, materials/guinardo-dossier.html
---

# Revisión de casos límite: PRD Wrapper FCF

Solo se recogen casos **no resueltos** por el PRD que piden una **decisión de producto**. Los detalles de implementación quedan para las specs. Formato de cada caso: **Escenario** → **Hoy (PRD)** → **Decisión** (con propuesta por defecto).

Veredicto: el camino feliz está bien cubierto y los casos límite más visibles ya tienen respuesta (rival sin partidos, acta pendiente, aplazado, despacho en Feed y calendario, contraste del Tema, contador de sanciones incierto). Los huecos graves están en tres zonas: **(1) fugas de identidad de menores** que la regla "por Competición" no tapa, **(2) cómo afectan a las Estadísticas avanzadas y al Dossier los datos que la FCF corrige o deja incompletos**, y **(3) qué pasa con seguimientos, Gestores y Dossiers cuando cambian la Temporada, la fase o el rol**.

Resumen: 4 críticos · 9 altos · 16 medios · 8 bajos.

---

## Crítico

### EC-C1. Un menor en una Competición de adultos, o el mismo Jugador en un Equipo de menores y en uno de adultos
- **Escenario:** un juvenil del Guinardó (17 años) juega en el Juvenil A (Competición de menores) y, desde enero, también con el Guinardó A en Quarta Catalana. En la Quarta sale con nombre completo, en el Juvenil como "Q. A. V. #8". Si la Ficha de jugador (FR-9) une su Temporada (la FCF usa el mismo `jugadorId`, y `jugador-stats` agrega por jugador), la ficha con nombre lista también sus partidos del Juvenil, y eso deshace la anonimización de todo el Juvenil (mismo dorsal, mismos goles). Variante "grupo mixto": en ligas femeninas de adultos juegan chicas de 14-16 años; con la regla actual salen con nombre completo en alineaciones, en goleadores (FR-10) y en Joc net (FR-11).
- **Hoy (PRD):** FR-17 aplica la regla "según la Competición, no según la edad". No dice nada de cruzar fichas entre Competiciones ni de menores en Competiciones de adultos.
- **Decisión:** ¿la Ficha de jugador se limita a un Equipo o a una Competición, o agrega toda la Temporada? ¿Se acepta mostrar con nombre a menores que juegan en Competiciones de adultos?
- **Propuesta por defecto:** la Ficha de jugador y todas sus estadísticas se limitan al Equipo (y a la Competición) desde el que se abre. **Nunca** se enlaza ni se suma un perfil de menores con uno de adultos, ni en la interfaz ni en URLs o identificadores visibles. Mostrar con nombre a menores en Competiciones de adultos se acepta como riesgo conocido (la FCF lo publica), pero se añade a Q-2 en `client-questions.md` para validarlo legalmente, junto con el caso del fútbol femenino.

### EC-C2. El texto del comité de sanciones lleva el nombre completo del menor
- **Escenario:** la FCF publica en `/competition/sanciones` una sanción a un alevín: "ARUMÍ VALLALTA, QUIM: 2 partits de suspensió…". FR-12 la muestra, FR-31 la envía como notificación y FR-16 la usa en el Dossier.
- **Hoy (PRD):** FR-32 dice que los textos de sanciones se muestran "tal como vienen, sin traducir", y FR-17 dice que en menores nunca aparece el nombre completo. Las dos reglas chocan, y FR-31 solo anonimiza "al Jugador", no el texto.
- **Decisión:** ¿se muestra en menores el texto literal del comité?
- **Propuesta por defecto:** en Categorías de menores **nunca** se muestra el texto libre de la FCF (sanciones, observaciones del acta). Se muestran solo los datos estructurados (Jugador Anonimizado, Equipo, partidos de sanción, Jornada). Si no se pueden extraer con certeza, se muestra "sanción del comité" sin detalle. Hay que corregir FR-32 para que tenga esta excepción.

### EC-C3. Una Competición que no se sabe clasificar como de menores
- **Escenario:** aparece una Competición con un nombre poco habitual ("Lliga Promoció F7", "Femení Base", "Escola", "Copa Primavera Infantil", "Segona Divisió Femenina sub-16"…) y la regla del nombre (pregunta abierta 4) no la reconoce como de menores. Todos sus Jugadores salen con nombre completo en todas las pantallas, y ese contenido ya puede estar indexado, en notificaciones o en Enlaces compartidos.
- **Hoy (PRD):** el §9.4 deja para la spec "cómo identificar" una Categoría de menores. No dice qué hacer cuando la regla no tiene certeza.
- **Decisión:** ¿qué se hace por defecto ante la duda: anonimizar o mostrar el nombre?
- **Propuesta por defecto:** **fallar cerrado**. Se anonimiza toda Competición que la regla no marque de forma explícita como de adultos (Primera, Segona, Tercera, Quarta Catalana, Veterans, ligas femeninas de adultos…), con una lista de Competiciones de adultos que el Administrador puede ampliar. En F7, se anonimiza por defecto toda la Disciplina, salvo excepciones explícitas.

### EC-C4. Cualquiera que diga ser del cuerpo técnico se hace Gestor y accede a nombres de menores y a Dossiers
- **Escenario:** (a) un jugador o el delegado del Darna pide ser Gestor del "Guinardó A" con "soy segundo entrenador". El Administrador solo ve la relación declarada (FR-22), la aprueba y desde entonces el Darna lee los Dossiers que el Guinardó prepara contra él. (b) Un desconocido pide ser Gestor del Alevín A o de un Club entero y, por A-3, ve los nombres completos de todos los menores del Club.
- **Hoy (PRD):** FR-21 y FR-22 aprueban según la relación declarada, sin verificarla. A-3 da los nombres completos de menores a cualquier Gestor del Equipo, y el §3.1 admite que un Gestor "puede ser un aficionado". La promesa de UJ-3, "nadie del rival puede verlo", depende de este filtro.
- **Decisión:** ¿cómo se verifica a un Gestor? ¿Ver nombres de menores depende de ser Gestor?
- **Propuesta por defecto:** (1) A-3 se invierte: **nadie ve nombres completos de menores en la app**, tampoco los Gestores, porque ya los tienen fuera de la app. (2) Si un Equipo ya tiene Gestores, una nueva Solicitud se les notifica y el Administrador no la aprueba sin consultarles. (3) Para el primer Gestor de un Club, el Administrador exige una prueba fuera de la app (correo del club o contacto directo), y el PRD lo dice de forma explícita. (4) Ser Gestor de un Club entero requiere ser de la junta.

---

## Alto

### EC-H1. Resultados de despacho, incomparecencias, partidos suspendidos y Equipos retirados en las Estadísticas avanzadas
- **Escenario:** Poble Nou – Barcelona Sporting: en el campo 0-1, de despacho 3-0. Luis, en su dossier, lo **excluye** de "marcó primero" ("0 de 3") y cuenta los goles por Tramo "en el campo". Otros casos que pasan cada temporada: (a) incomparecencia, un 3-0 sin alineaciones ni goles; (b) partido suspendido en el minuto 60 (lluvia o incidentes) que se reanuda otro día o se resuelve en el comité; (c) un Equipo que se retira a mitad de temporada y cuyos resultados la FCF anula, lo que recalcula la clasificación de todos.
- **Hoy (PRD):** FR-3 y FR-5 solo dicen cómo **mostrar** el despacho. FR-13, FR-14, FR-15, FR-8 y la racha de FR-4 no dicen si usan el resultado oficial o el del campo. El glosario solo tiene tres estados de Partido (programado, aplazado, jugado), así que faltan "suspendido", "no presentado" y "anulado".
- **Decisión:** la regla para cada métrica y los estados que faltan.
- **Propuesta por defecto:** puntos, clasificación, racha y "ganó" usan el **resultado oficial**. Goles por Tramo, quién marca primero, goleadores, tarjetas y titularidades usan **lo que pasó en el campo**. Un Partido sin juego real (incomparecencia, anulado) no cuenta en el denominador de "Partidos jugados" para las estadísticas de Jugadores ni en quién marca primero. Cada métrica en la que se excluye algún Partido lo indica ("calculado sobre 3 de 4 partidos"). Se añaden los estados "suspendido", "no presentado" y "anulado (equipo retirado)". El Equipo retirado sigue en el Feed con un aviso "retirado de la competición".

### EC-H2. Actas corregidas y resultados que cambian después de publicarse
- **Escenario:** el sábado a las 22:00 la FCF publica 2-1. El lunes corrige el acta (un gol pasa a otro Jugador, se quita una roja) o, semanas después, el comité cambia el resultado a uno de despacho. Además, la FCF puede publicar el resultado en `partidos` antes de cerrar el acta (`CERRADA=0`), con datos parciales.
- **Hoy (PRD):** FR-28 avisa una vez ("no se envía el mismo aviso dos veces"). No dice qué pasa si el resultado cambia, ni si se muestra un acta sin cerrar. SM-4 ("cero discrepancias") cuenta como fallo enseñar algo que luego cambia.
- **Decisión:** ¿se muestra un acta sin cerrar? ¿Se avisa cuando cambia un resultado ya avisado?
- **Propuesta por defecto:** un resultado sin acta cerrada se muestra con la etiqueta "provisional" y no genera estadísticas de Jugador. Las estadísticas solo usan actas cerradas. Si cambia el **marcador oficial** de un Partido ya avisado, se envía un único aviso "resultado modificado" (o "resultado de despacho"). Las correcciones menores (goleador, tarjetas) se aplican sin aviso. Las estadísticas, la Plantilla y los Dossiers se recalculan siempre.

### EC-H3. ¿El Dossier es una foto o un informe vivo?
- **Escenario:** el lunes el Gestor pide el Dossier del Darna para el sábado. El miércoles el Darna juega un aplazado, el jueves el comité sanciona a su portero y el viernes la FCF corrige un acta. El sábado el cuerpo técnico abre el Enlace privado. Con una foto, ve datos del lunes sin saberlo. Con un informe vivo, el contenido ha cambiado sin aviso y no coincide con lo que se habló en la reunión del martes.
- **Hoy (PRD):** FR-24 dice "disponible en minutos". No dice si se actualiza, y no lleva fecha de los datos (el dossier manual de Luis indica "Datos FCF a 19/10/2026").
- **Decisión:** ¿foto o informe vivo? ¿Qué fecha de datos se muestra?
- **Propuesta por defecto:** el Dossier es **vivo** hasta que empieza el Partido y queda fijo a partir de ese momento. Siempre muestra "Datos FCF a {fecha y hora}" y marca lo nuevo desde que se pidió ("nueva sanción", "+1 partido jugado"). El "próximo Partido" de FR-25 es **el Partido contra el Equipo que pidió el Dossier**, no el siguiente que juegue el rival.

### EC-H4. El Partido del Dossier se aplaza (una vez, dos veces o sin fecha)
- **Escenario:** el Enlace privado "caduca al terminar el Partido" (A-5). El Partido se aplaza sin fecha y el enlace no caduca nunca. Si se reprograma dos veces, el enlace caduca a la hora original, cuando el Partido aún no se ha jugado. El Gestor también puede querer un Dossier de un Partido que ya se jugó (FR-24 dice "cualquier Partido de liga").
- **Hoy (PRD):** A-5 no tiene en cuenta los aplazamientos, y FR-24 no limita los Partidos ya jugados.
- **Decisión:** ¿cuándo caduca el enlace si cambia la fecha? ¿Se puede pedir el Dossier de un Partido ya jugado?
- **Propuesta por defecto:** el enlace caduca cuando la FCF publica el resultado de **ese** Partido o, si no hay resultado, a los 14 días de crearse. Se renueva solo si el Partido se reprograma. Solo se pueden pedir Dossiers de Partidos no jugados. Los ya generados se siguen pudiendo consultar en modo lectura y fijos.

### EC-H5. Se retira a un Gestor (o deja de serlo) mientras hay Enlaces privados compartidos
- **Escenario:** el Administrador retira el rol al segundo entrenador, que se ha ido al Darna, o cambia de temporada. Los enlaces que ese Gestor generó siguen abiertos y circulando por WhatsApp. Además, no se sabe si los Dossiers que pidió siguen visibles para los otros Gestores del Equipo.
- **Hoy (PRD):** FR-22 permite retirar el rol y FR-27 deja que el Gestor revoque sus enlaces. No dice qué pasa con los enlaces y los Dossiers de un Gestor retirado, ni si otro Gestor puede revocarlos.
- **Decisión:** ¿de quién son los Dossiers y los enlaces: del Gestor o del Equipo?
- **Propuesta por defecto:** los Dossiers son **del Equipo**: siguen visibles para sus Gestores y cualquiera de ellos puede revocar cualquier enlace. Al retirar a un Gestor se revocan automáticamente los enlaces que él generó. El Gestor de Club puede revocar los de todos sus Equipos.

### EC-H6. El Equipo juega la liga en dos Grupos (segunda fase)
- **Escenario:** en fútbol base, sobre todo en F7 (alevín, benjamín) y en algunas categorías de F11, la liga tiene una primera fase y en enero los Equipos se reparten en Grupos nuevos según su nivel. El Alevín A que sigue Núria (UJ-4) cambia de Grupo y de rivales a mitad de temporada, y su Grupo de la primera fase se queda sin partidos.
- **Hoy (PRD):** el glosario dice que "un Equipo juega la liga en un Grupo". Los fuera de alcance excluyen "fases de ascenso", pero esto es la propia liga.
- **Decisión:** ¿qué Grupo es "la liga" del Equipo? ¿Las estadísticas se calculan por fase o para toda la Temporada?
- **Propuesta por defecto:** el Equipo sigue con su mismo seguimiento y la app muestra el **Grupo activo** (el de la fecha más reciente). Las fases anteriores se ven como "Fase 1" en el calendario. La clasificación es la del Grupo activo. La Plantilla y las estadísticas de Jugador son de toda la Temporada. Las Estadísticas avanzadas y el Dossier se calculan por fase, con un selector.

### EC-H7. Cambio de Temporada: seguimientos, Gestores, Dossiers y verano sin datos
- **Escenario:** en julio de 2027 termina la temporada 2026-27, y la FCF publica los Grupos 2027-28 entre agosto y septiembre. (a) En verano, ¿qué es la "Temporada en curso" y qué muestra el Feed? (b) Si el Equipo de la temporada anterior no existe en la nueva (el Guinardó B pasa a ser el C, desaparece o desciende), el seguimiento queda colgado. (c) No se sabe si el Gestor del Guinardó A en 2026-27 lo sigue siendo en 2027-28. (d) Si un Equipo está inscrito pero aún no tiene Grupo ni calendario, el Feed no tiene qué mostrar.
- **Hoy (PRD):** "la v1 muestra la Temporada en curso" y Equipo se define "por Temporada". No hay regla de transición.
- **Decisión:** la regla de cambio de Temporada.
- **Propuesta por defecto:** la Temporada anterior se muestra (fija, con la etiqueta "temporada finalizada") hasta que la FCF publica el calendario del Equipo en la nueva. El seguimiento se traslada solo al Equipo del mismo Club con el mismo nombre y Disciplina. Si no existe, el Feed lo indica y propone los Equipos del Club. El rol de Gestor pasa automáticamente al Equipo equivalente, y el Administrador puede revocarlo. Los Dossiers de la temporada anterior se archivan en solo lectura. Un Equipo sin calendario muestra "calendario pendiente de publicar por la FCF".

### EC-H8. Árbitros, técnicos y delegados menores de edad
- **Escenario:** en los partidos de base, y también en Quarta Catalana, arbitran a menudo chicos de 15-17 años, y los segundos entrenadores o delegados de un alevín pueden ser juveniles. FR-7 muestra "árbitros… y cuerpo técnico" con nombre completo.
- **Hoy (PRD):** FR-17 solo anonimiza a "los Jugadores".
- **Decisión:** ¿qué se muestra de árbitros y técnicos?
- **Propuesta por defecto:** en Categorías de menores, los árbitros y el cuerpo técnico se muestran Anonimizados (iniciales y rol). En adultos, el árbitro principal se muestra solo con iniciales y rol. No se crean fichas ni rankings de árbitros (ya está fuera de alcance buscar árbitros, pero hay que extender esa exclusión a cualquier vista que los liste).

### EC-H9. La FCF cae o cambia el formato de la API
- **Escenario:** (a) el sábado por la noche `fcf.cat/api` devuelve 500 durante horas: el Feed no tiene resultados, FR-33 (una hora) no se cumple y el Gestor no puede generar el Dossier del lunes. (b) La FCF renombra un campo (`GOLES_FUERA` → `GOLS_FORA`) o cambia `tipo_gol`, y la app calcula en silencio 0 goles o mal los goles por Tramo, lo que rompe SM-4.
- **Hoy (PRD):** el §2 reconoce el riesgo y FR-33 promete una hora. No dice qué ve el usuario cuando los datos no están al día ni qué se prefiere entre datos viejos y datos dudosos.
- **Decisión:** ¿qué ve el usuario con datos desactualizados o dudosos?
- **Propuesta por defecto:** cada pantalla de datos muestra "Actualizado hace X". Si la última sincronización correcta tiene más de 2 horas, aparece un aviso "La FCF no responde; datos a {hora}". Ante datos con forma inesperada, **se prefiere el dato viejo al dudoso**: se congela el último dato bueno y se avisa al Administrador. Un Dossier pedido sin conexión con la FCF se genera con los últimos datos y su fecha, o queda en "pendiente" y avisa al Gestor cuando está listo.

---

## Medio

### EC-M1. Actas incompletas: goles sin minuto, sin goleador o partidos sin acta
- **Escenario:** en base es habitual encontrar actas con goles sin minuto (o con minuto 0), goles sin Jugador asignado o Partidos con resultado y sin acta. La suma de goles por Tramo (FR-14) o de goles de la Plantilla no coincide con los GF de la clasificación (FR-4/FR-6), y un usuario lo ve como una discrepancia (SM-4).
- **Hoy (PRD):** FR-9 exige que los totales "coincidan con la suma de las Actas", pero no qué hacer si las Actas no cuadran con la clasificación.
- **Propuesta por defecto:** cada métrica calculada a partir de Actas indica su cobertura ("12 de 14 goles con minuto"; "calculado con 4 de 5 actas"). La clasificación y los GF/GC salen siempre de la FCF y nunca se recalculan.

### EC-M2. Identidad Anonimizada inestable: el dorsal cambia, se repite o las iniciales coinciden
- **Escenario:** en el dossier de Luis, el Torre Fuerte tiene dos #23 (D'Oleo y Caceres) y dos #14, y en el Darna hay dos #9 y dos #2. En menores, "iniciales + dorsal" puede dar dos "M. E. #6" distintos, o un mismo niño que aparece como #8 y como #12 en dos Jornadas. Los nombres de la FCF también llegan truncados ("Mohamed El", "Oriol"). Una familia que busca a su hijo (JTBD "los de su hijo") no lo encuentra o lo confunde.
- **Hoy (PRD):** FR-17 dice "iniciales y dorsal", sin decir qué dorsal.
- **Propuesta por defecto:** la identidad interna es el `id` de la FCF. La etiqueta pública usa las iniciales y el dorsal **más usado** en la Temporada. Si dos Jugadores del mismo Equipo coinciden en la etiqueta, se añade una letra o un número ("M. E. #6 (2)"). En la tabla por Jornada se muestra el dorsal de cada Partido.

### EC-M3. El mismo Jugador en dos Equipos del Club o traspasado a mitad de temporada (adultos)
- **Escenario:** un jugador del Guinardó B juega 3 partidos con el A, o un jugador del Darna ficha por el River Plate en el mercado de invierno. FR-8 lo cuenta en las dos Plantillas. El "once más repetido" del rival (FR-15) incluye a alguien que ya no está, y en la Ficha de jugador (FR-9) no queda claro qué partidos son de qué Equipo.
- **Hoy (PRD):** no se dice nada (la parte de menores está en EC-C1).
- **Propuesta por defecto:** la Plantilla es por Equipo. Si un Jugador lleva 3 o más Jornadas sin aparecer y ha aparecido después en otro Equipo, se marca como "ya no está (último partido J8)" y sale del once más repetido del Dossier. Cuando la Ficha de jugador es de adultos, muestra cada Equipo por separado.

### EC-M4. Orden por Jornada u orden cronológico, cuando hay aplazados
- **Escenario:** la J3 del Guinardó (aplazada) se juega el 19/10, después de la J5. La "racha de los últimos 5" (FR-4/FR-6), el "debutante en el último Partido" (FR-8) y "Partidos jugados desde" la sanción (FR-16) cambian según se ordene por Jornada o por fecha. Un jugador que debuta en la J3 el 19/10 tiene su primer partido en una columna anterior a otras en las que ya ha jugado.
- **Hoy (PRD):** FR-4 ordena por fecha solo el "próximo Partido".
- **Propuesta por defecto:** la racha, el debutante, el "último Partido" y las sanciones van por **fecha de juego**. La tabla de la Plantilla mantiene las columnas por Jornada y marca la fecha del aplazado.

### EC-M5. Jornada de descanso en Grupos impares
- **Escenario:** el Grup 20 tiene 15 Equipos, así que cada Jornada descansa uno. En la tabla por Jornada (FR-8) el descanso no se puede mostrar como "No convocado" para toda la Plantilla. Si el Equipo descansa en la siguiente Jornada, el "próximo Partido" del Feed puede estar a dos semanas sin explicación.
- **Hoy (PRD):** no se dice nada.
- **Propuesta por defecto:** se añade el estado "Descansa". La tabla muestra la columna en gris, el calendario muestra "J7 · descansa" y el Feed muestra "Descansa esta jornada · próximo: …".

### EC-M6. Partido sin hora fijada y zona horaria
- **Escenario:** la FCF publica el calendario con fecha y sin hora (en la API llega como `T00:00:00`). La app muestra "00:00" y el recordatorio de FR-30 se envía a las 21:00 del día anterior. Además, `acta.COMIENZO1` llega con `Z` aunque sea hora local: un móvil configurado en otra zona horaria (una familia de fuera) o el cambio de hora del 25/10/2026 desplazan la hora mostrada.
- **Hoy (PRD):** no se dice nada (ENDPOINTS.md avisa de que no hay que convertir la hora).
- **Propuesta por defecto:** las 00:00 se interpretan como "hora por confirmar" y en ese caso no se envía recordatorio. Las horas se muestran **siempre en hora de Catalunya**, sin importar la zona del dispositivo.

### EC-M7. Aplazado sin fecha nueva, y reprogramado dos veces
- **Escenario:** la J3 se aplaza sin fecha. FR-4 lo pone como próximo "según su fecha", pero no tiene fecha. El Feed ordena "en orden cronológico" y no sabe dónde colocarlo. Si se reprograma A→B y después B→A, no queda claro si el segundo cambio es "el mismo aviso" (FR-29) que no se debe repetir. Si se aplaza 2 horas antes, ya se ha enviado el recordatorio de las 3 horas.
- **Hoy (PRD):** FR-3/FR-5 lo marcan como aplazado, pero no dicen dónde va en el orden ni cómo se avisa.
- **Propuesta por defecto:** los aplazados sin fecha van en una franja "Pendientes de fecha" encima del Feed, y el "próximo Partido" es el siguiente con fecha. Cada cambio de fecha, hora o campo es un aviso distinto (la deduplicación se aplica al mismo cambio, no a la misma fecha). Un aplazamiento después del recordatorio genera siempre el aviso.

### EC-M8. Avalancha de notificaciones al seguir un Equipo y partidos entre dos Equipos seguidos
- **Escenario:** (a) al seguir un Equipo o al crear la Cuenta, la primera carga de datos "descubre" 5 resultados y 3 sanciones y envía 8 avisos. Lo mismo pasa si la FCF reescribe en bloque las horas de una Jornada. (b) Núria sigue al Guinardó A y al Darna: recibe dos avisos del mismo Partido, y en el Feed (UJ-4) el Partido aparece dos veces o no se sabe qué Tema lleva la tarjeta.
- **Hoy (PRD):** FR-28 a FR-31 no dicen nada de esto.
- **Propuesta por defecto:** solo se avisa de hechos detectados **después** de que el usuario siga el Equipo, y como máximo un aviso agrupado por Equipo y hora. Un Partido entre dos Equipos seguidos sale una sola vez en el Feed (con los colores del Equipo local o en tarjeta partida) y genera un solo aviso.

### EC-M9. Once más repetido con empates o sin portero claro
- **Escenario:** en el Darna, Ouzzine y Reina tienen 2/4 titularidades como porteros, y en el puesto 11 empatan varios jugadores con 3/4. Luis eligió a mano (un solo portero). Con el criterio de FR-15 (los 11 con más titularidades) pueden salir 0 o 2 porteros, o 13 jugadores empatados.
- **Hoy (PRD):** FR-15 no lo resuelve.
- **Propuesta por defecto:** siempre hay 1 portero (el que más veces ha sido titular como portero) y 10 (o 6 en F7) jugadores de campo. Los empates se deshacen por convocatorias y, después, por titular en el último Partido. Si hay empate en el último puesto, se indica "empatado con X".

### EC-M10. Estados vacíos fuera del Dossier
- **Escenario:** (a) antes de la J1, la Ficha de equipo muestra Estadísticas avanzadas, rankings y Plantilla vacíos. (b) Al elegir un Club solo de fútbol sala, no hay Equipos de la v1. (c) El Equipo está inscrito y la FCF aún no le ha asignado Grupo.
- **Hoy (PRD):** solo se cubre el caso del Dossier sin partidos (FR-24).
- **Propuesta por defecto:** se aplica la misma regla que en el Dossier a la Ficha de equipo y a los rankings ("aún no hay partidos jugados"). Si el Club no tiene Equipos de F11, F7 o Femení, aparece el mensaje "Este club no tiene equipos de las disciplinas disponibles". Un Equipo sin Grupo muestra "pendiente de que la FCF publique el grupo".

### EC-M11. Categorías en las que la FCF no publica clasificación o resultados
- **Escenario:** si la FCF no publica clasificación (o goleadores) en las categorías más pequeñas (p. ej. prebenjamín o benjamín) para no fomentar la competitividad, la app, al calcular racha, rankings y Estadísticas avanzadas a partir de las Actas, publicaría lo que la federación ha decidido ocultar.
- **Hoy (PRD):** no se dice nada. FR-6 se limita a "lo que indica la FCF" en ascensos y descensos.
- **Propuesta por defecto:** la app **nunca calcula** para una Competición más de lo que la FCF publica en ella. Si no hay clasificación oficial, no se muestran clasificación, racha, rankings ni Estadísticas avanzadas. Se comprueba en la spec qué Competiciones están en este caso.

### EC-M12. Varios Gestores pidiendo el Dossier a la vez, y Gestor de Club frente a Gestor de Equipo
- **Escenario:** dos Gestores del Guinardó A piden a la vez el Dossier del Darna. No está claro si tienen que salir uno o dos Dossiers ni quién controla los enlaces. Un Gestor de Club y uno de Equipo pueden revocarse los enlaces el uno al otro.
- **Hoy (PRD):** FR-26 dice "los Gestores del Equipo que lo pidió", lo que deja entender que es uno compartido, pero no lo concreta.
- **Propuesta por defecto:** hay un solo Dossier por Equipo y Partido, compartido entre todos sus Gestores. Pedirlo otra vez lo refresca. Se ve quién generó cada enlace.

### EC-M13. El Administrador también es Gestor de un Equipo
- **Escenario:** Luis es Administrador y Gestor del Guinardó A. Puede aprobarse a sí mismo como Gestor del Darna, o tener acceso técnico a los Dossiers que los rivales preparan contra el Guinardó. Para abrir la app a otros clubs ("listo para otros clubs"), estos tienen que poder confiar en que el dueño de la app no los espía.
- **Hoy (PRD):** FR-26 no menciona al Administrador.
- **Propuesta por defecto:** el rol de Administrador **no** da acceso a Dossiers de otros Equipos. El Administrador no puede aprobar sus propias Solicitudes ni ser Gestor de dos Equipos del mismo Grupo. Esta política se publica en la app.

### EC-M14. Marca manual: conflictos y moderación
- **Escenario:** dos Gestores del mismo Equipo cambian a la vez la Marca. El Gestor de Club pone una Marca y el del Equipo otra. Un "aficionado" Gestor sube un logo ofensivo o el de otro club. Si se retira al Gestor, no está claro si su Marca se mantiene. Además, FR-18 garantiza la legibilidad del Tema, pero no de la Marca.
- **Hoy (PRD):** FR-19 sustituye el Tema "para todos los Seguidores", sin revisión.
- **Propuesta por defecto:** la Marca de Equipo prevalece sobre la de Club. Gana el último cambio y queda en un historial. El Administrador puede volver al Tema automático con un clic. La regla de contraste de FR-18 se aplica también a la Marca, y la Marca se mantiene aunque se retire al Gestor.

### EC-M15. Rankings de la FCF que no cuadran con lo que la app calcula de las Actas
- **Escenario:** el pichichi de la FCF (`/goleadores`, FR-10) da 5 goles a Farouki y la Plantilla calculada de las Actas (FR-8) le da 4, porque una corrección de la FCF solo se aplicó a uno de los dos lados o porque hay un despacho por medio. El usuario ve dos cifras distintas en la app.
- **Hoy (PRD):** FR-10 a FR-12 usan los datos de la FCF y FR-8/FR-9 los calculan de las Actas. No dice qué cifra prevalece.
- **Propuesta por defecto:** los rankings del Grupo se muestran tal como los da la FCF, y lo calculado de las Actas lleva la etiqueta "según actas". Las diferencias se registran para el Administrador, no se corrigen a mano.

### EC-M16. Goles en propia puerta y penaltis
- **Escenario:** la FCF registra un gol en propia de un jugador del Darna. No se sabe si cuenta en sus goles de la Plantilla, a qué Equipo se le asigna en goles por Tramo y en "marca primero", ni si aparece en goleadores. Los códigos aún no se han visto (ENDPOINTS.md).
- **Hoy (PRD):** no se dice nada.
- **Propuesta por defecto:** un gol en propia cuenta a favor del Equipo que se beneficia (Tramos, marca primero), sin goleador, y no se suma al Jugador que lo marca. Los penaltis cuentan como gol normal y se marcan como "de penalti".

---

## Bajo

### EC-L1. Equipos con el mismo nombre en Disciplinas distintas
Si el Club tiene un "Guinardó A" en F11 y otro en Femení, Núria ve dos tarjetas iguales en el Feed. **Propuesta:** cuando dos Equipos seguidos se llaman igual, las tarjetas y el título de la Ficha muestran la Disciplina o la Categoría ("Femení", "Alevín").

### EC-L2. Se pierden los Equipos seguidos sin Cuenta
En el Hito 1 no hay Cuentas. Safari (sin instalar la app) borra los datos del sitio tras 7 días sin uso, y el usuario también puede borrar el navegador: pierde sus seguimientos sin aviso. Al iniciar sesión en un dispositivo que ya tiene seguimientos locales, no se sabe si se unen o se sustituyen. **Propuesta:** se aceptan las pérdidas en el Hito 1 y la app invita a instalarla. Al iniciar sesión, los seguimientos locales y los de la Cuenta se unen.

### EC-L3. Retirada de nombres a petición
Un jugador adulto o un club (Q-2 solo cubre la base del Guinardó) pide que se quite su nombre o su Equipo. Las fichas de Jugador pueden aparecer en buscadores. **Propuesta:** el Administrador puede anonimizar a un Jugador o a un Equipo concreto a petición, y las fichas de Jugador no se indexan en buscadores.

### EC-L4. Dos Equipos del mismo Club en el mismo Grupo
En base es habitual que el A y el B del Club compartan Grupo. El Gestor del B puede pedir el Dossier del A, y el Gestor de Club ve los dos. **Propuesta:** está permitido. El Dossier sigue siendo del Equipo que lo pide, y el Gestor de Club ve los dos (no hay "rival" que proteger dentro del Club).

### EC-L5. Solicitudes duplicadas o repetidas
Un usuario pide ser Gestor de un Equipo cuyo Club ya gestiona, insiste después de un rechazo, o su Solicitud sigue pendiente semanas porque el Administrador es una sola persona. **Propuesta:** no se puede pedir lo que ya se tiene. Tras un rechazo hay que esperar 30 días para volver a pedir. El Administrador recibe un recordatorio de las Solicitudes pendientes desde hace más de 3 días, y la Solicitud muestra el motivo del rechazo.

### EC-L6. Recordatorio a horas intempestivas
Con un Partido a las 9:00, el recordatorio de 3 horas (A-6) llega a las 6:00. **Propuesta:** el recordatorio nunca se envía antes de las 8:00. Si tocaría antes, se envía a las 20:00 del día anterior.

### EC-L7. Gol en el añadido de la primera parte
El acta da el minuto 47 y no se puede saber si es el 45+2 o el minuto 2 de la segunda parte, pero FR-14 dice que los goles del añadido van "en el último Tramo de su parte". **Propuesta:** se aplica el minuto tal cual (47 → 46-60) y se documenta como limitación de la fuente.

### EC-L8. Tema sin datos de equipación o escudo
Un Equipo nuevo o una fila duplicada o vacía en `/equipacions` deja el Equipo sin colores o sin escudo, pero FR-18 promete "Tema sin intervención humana". **Propuesta:** si no hay colores, se usa un Tema neutro de la app, y si no hay escudo, las iniciales del Club. Si hay filas duplicadas, se usa la primera equipación completa.

---

## Nota sobre el material de partida

El dossier manual de Luis cubre **los 3 próximos rivales y la ficha propia** ("Nuestra ficha", tabla comparativa de goles). FR-24/FR-25 lo reducen a un rival por petición y sin ficha propia. En semanas con un aplazado entre semana más el partido del fin de semana (como la del 19/10 al 24/10), el Gestor tendría que pedir dos Dossiers. No es un caso límite, pero vale la pena confirmar con Luis que la reducción es intencionada, porque afecta a SM-3 (menos de 10 minutos para preparar al rival).
