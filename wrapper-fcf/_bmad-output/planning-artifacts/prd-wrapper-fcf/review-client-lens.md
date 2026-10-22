---
title: 'Revisión client-lens — PRD Wrapper FCF'
reviewed: prd.md (draft, 2026-10-22)
contra: .decision-log.md (L1–L56), materials/guinardo-dossier.html (texto visible), client-questions.md
fecha: 2026-10-22
---

# Revisión client-lens — PRD Wrapper FCF

**Veredicto:** el PRD es fiel a la gran mayoría de decisiones de Luis (roles, disciplinas, hitos, menores, idioma, export por enlace, non-goals, notificaciones) y cubre casi todos los bloques del dossier. Pero **pierde la decisión que debe condicionar la arquitectura desde v1** (qué se paga y quién lo ve), deja **una contradicción interna en la privacidad del Dossier** (FR-26 vs FR-27) y **no recoge una regla de cálculo que el dossier de Luis sí aplica** (los Resultados de despacho no cuentan en las estadísticas "de campo"). El resto son ajustes de precisión y supuestos del PM sin etiquetar.

Recuento: **1 crítico · 2 altos · 9 medios · 10 bajos.**

Referencias: `DL-n` = línea n de `.decision-log.md`; `PRD-n` = línea n de `prd.md`; "Dossier" = texto visible de `guinardo-dossier.html`.

---

## CRÍTICO

### C-1. El modelo de pago futuro queda reducido a "desbloquear funciones" y se pierde quién ve lo pagado
- **Evidencia (Luis):**
  - DL-14: "debe estar preparado para que alguien pague por dar de alta un club con sus estadísticas. Quien paga puede ser **un seguidor** o una persona que gestiona un club entero. […] el modelo de roles debe soportarla **desde v1**".
  - DL-22: "las estadísticas avanzadas pagadas para un club/equipo **las ven TODOS sus seguidores (patrocinio)**. El dossier de scouting solo lo ve quien gestiona".
  - DL-23: "plan por equipo y plan por club entero, **con precios distintos**".
- **Lo que dice el PRD:**
  - PRD-21: "un **Gestor** pague por desbloquear funciones para su Equipo o Club".
  - PRD-40: Gestor "En el futuro será quien pague un Plan".
  - PRD-265 (FR-23): "un Plan de pago por Equipo o por Club desbloquee funciones […] La aprobación de la Solicitud de gestión es el punto donde irá el pago".
  - PRD-83 (Plan): "desbloquea funciones para un Equipo o un Club entero".
- **Problema:** el PRD no dice *qué* se paga (las Estadísticas avanzadas, que en v1 son gratis y abiertas, DL-32) ni que el derecho es **del Equipo/Club y lo disfrutan todos sus Seguidores** (patrocinio), no solo quien paga. Tal como está FR-23, una spec construiría derechos ligados al usuario Gestor, que es justo lo que habría que rehacer. Tampoco recoge que el pagador puede ser un seguidor (el PRD lo resuelve implícitamente con "el Gestor puede ser un aficionado", PRD-40, pero no lo dice), ni los precios distintos por Equipo / Club. Además hay una consecuencia no tratada: si en el futuro las Estadísticas avanzadas del rival solo existen cuando el rival (o su club) paga, ¿qué incluye el Dossier de un rival que no ha pagado?
- **Arreglo sugerido:** reescribir FR-23 con consecuencias testeables:
  - "El derecho de un Plan pertenece a un Equipo (Plan de Equipo) o a todos los Equipos de un Club (Plan de Club), con precios distintos."
  - "Lo que desbloquea un Plan (las Estadísticas avanzadas, en el modelo previsto) lo ven **todos** los Seguidores de ese Equipo, con o sin Cuenta."
  - "El Dossier sigue siendo solo de los Gestores aunque haya Plan."
  - "Puede pagar cualquier usuario con Cuenta; al pagar pasa a Gestor (la aprobación de la Solicitud es el punto de pago)."
  - Añadir pregunta abierta: "Dossier de un rival sin Plan: ¿incluye sus Estadísticas avanzadas?".
  - Alinear PRD-21, PRD-40 y el glosario (Plan) con esto.

---

## ALTO

### H-1. FR-26 contradice FR-27 y el propósito "que no llegue al rival"
- **Evidencia:** DL-22 "solo lo ve quien gestiona, **para que no llegue al rival**"; DL-27 "Solo lo ve el Gestor"; DL-52 "Exportación del dossier: enlace privado (no PDF)".
- **PRD:** FR-26 (PRD-285) "Solo los Gestores del Equipo que pidió el Dossier pueden verlo. Ningún Seguidor…". FR-27 / A-5 (PRD-288) "quien tiene el enlace lo abre sin Cuenta".
- **Problema:** las dos consecuencias no pueden ser ciertas a la vez: un Enlace privado que se abre sin Cuenta lo ve cualquiera que lo reciba, incluido un Seguidor o alguien del rival si se reenvía por WhatsApp. El PRD resuelve la tensión con un supuesto (A-4, "todo el cuerpo técnico puede ser Gestor") que va en sentido contrario a A-5.
- **Arreglo sugerido:** que Luis elija una de dos opciones y reescribir FR-26 en consecuencia:
  - **(a)** El enlace solo se abre con Cuenta de un Gestor del Equipo. Es lo más fiel a DL-22, y entonces A-4 es necesario.
  - **(b)** El enlace se abre sin Cuenta, y FR-26 dice "solo Gestores **y quien tenga un Enlace privado vigente**", con revocación, caducidad y aviso de que reenviar el enlace lo expone.

  Con (b), A-5 deja de ser un supuesto menor y pasa a ser decisión de producto.

### H-2. Falta la regla de cómo cuentan los Resultados de despacho en las Estadísticas avanzadas
- **Evidencia (Dossier, Poble Nou):** "J2 Barcelona Sporting Casa 3-0\* · \* Resultado de despacho: en el campo fue 0-1"; "**Marcó primero en 0 de 3**" con 4 PJ; Claves: "En el campo llevan 3 goles en 4 partidos, y en todos marcó primero el rival"; "Encajan poco: 6 goles **en el campo**". Los Tramos de Poble Nou suman 3 a favor, que son los goles de campo, no los 5 oficiales.
- **PRD:** FR-5 y FR-25 muestran el resultado de despacho, pero FR-13, FR-14 y FR-15 no dicen si usan el resultado oficial o los hechos del Acta de campo. FR-4 y FR-6 usan el oficial, porque la clasificación debe coincidir con la FCF.
- **Problema:** el Dossier hecho a mano por Luis es la referencia de aceptación, y la app daría números distintos ("marcó primero en X de 4" en vez de "de 3"; GF por Tramo inflados con goles que no existen). Además choca con la counter-metric SM-4 (cero discrepancias).
- **Arreglo sugerido:** añadir en §5.7 una consecuencia común:
  - "Clasificación, puntos y GF/GC del resumen usan el resultado oficial. Quién marca primero, goles por Tramo, once y plantilla usan los hechos del Acta de campo. Un Partido con Resultado de despacho se excluye del denominador de 'marca primero' si no tiene hechos de campo coherentes, y la app indica cuántos Partidos se han excluido."
  - Que Luis confirme la regla.

---

## MEDIO

### M-1. "Once más repetido" no reproduce el criterio del dossier (portero y capitanes)
- **Evidencia (Dossier, Darna):** el once lo encabeza "Hamid Ouzzine **Portero** · 2/4 tit.", aunque hay seis jugadores de campo con 3/4. Siempre aparece un único portero, y el otro portero (Reina, 2/4) no entra. Hay varios "cap." en el mismo once (Dia, Ezzouyn).
- **PRD:** FR-15 (PRD-213) "los 11 Jugadores (7 en Futbol 7) con más titularidades". Con esa regla, en Darna el portero quedaría fuera o empatado con jugadores de campo.
- **Arreglo:** "1 portero (el que tenga más titularidades como portero) + 10 (6 en F7) Jugadores de campo con más titularidades; desempate por convocatorias y luego por goles. 'Capitán' = ha sido capitán en algún Acta". La misma aclaración vale para FR-8 ("se indica el capitán"), porque el capitán cambia según el Acta.

### M-2. Del dossier se pierden "Nuestra ficha" y "Próximos rivales"
- **Evidencia (Dossier):** la navegación inferior es "Tabla · Goles · TFC 19/10 · DAR 24/10 · PBN 31/10 · Guinardó". La cabecera de cada rival dice "Próximos rivales · hasta el descanso". La leyenda de la clasificación: "Azul: próximos rivales (toca para verlos)". Hay una pestaña "Guinardó Almogàvers **Nuestra ficha**" con los mismos bloques del propio equipo más el debutante.
- **PRD:** FR-25 solo describe el rival (más la clasificación con propio y rival destacados). Luis eligió "un rival concreto" (DL-42), así que el informe multi-rival queda bien fuera, pero:
  - (a) no hay ningún sitio donde el Gestor vea "mis próximos rivales" para elegir.
  - (b) el Dossier no enlaza ni compara con la ficha propia, que en el manual va en el mismo documento.
- **Arreglo:**
  - FR-24: "al pedir un Dossier, el Gestor ve la lista de próximos Partidos de liga con rival, fecha y casa o fuera, y elige uno".
  - FR-25: "incluye un acceso a las Estadísticas avanzadas del propio Equipo (o un resumen comparativo propio vs rival)", o bien marcarlo explícitamente fuera de alcance.
  - Si se descarta el informe de varios rivales, añadirlo a §7.2.

### M-3. Falta el sello "datos a fecha"
- **Evidencia (Dossier):** "Tras la jornada 5 · **Datos FCF a 19/10/2026**".
- **PRD:** no lo menciona ni en FR-25 ni en FR-33. Un Dossier compartido por enlace se abre días después y hay que saber a qué fecha corresponde.
- **Arreglo:** consecuencia en FR-25 y FR-33: "Dossier, clasificación y estadísticas muestran 'tras la Jornada N · datos FCF a dd/mm hh:mm'".

### M-4. La "Primera entrega 23/10" cuadra en contenido pero no es verificable
- **Evidencia:** DL-39 "la app básica en Vercel solo para el Guinardó A (**inicio**, calendario y resultados, clasificación, fichas de partido, plantilla con estadísticas; sin cuentas ni dossier)"; DL-40 "NO vía rápida […] aunque eso comprometa la entrega de mañana".
- **PRD-348:** "resumen, calendario y resultados, clasificación, Fichas de partido y plantilla con estadísticas". El contenido coincide, pero:
  - "inicio" se ha traducido a "resumen" sin decirlo. En DL-41 "Inicio" pasa a ser el Feed. Hay que fijar que mañana la pantalla de entrada es el resumen del Guinardó A, sin búsqueda, sin seguir y sin Feed.
  - No se citan los FR (FR-4, FR-5, FR-6, FR-7, FR-8) ni qué consecuencias quedan aplazadas. ¿Entran la tabla T/S/– y el debutante de FR-8? ¿Hace falta ca/es (FR-32), el Tema (FR-18), la frescura de 1 h (FR-33) o la atribución (FR-34)?
  - No dice que se aceptó el riesgo de que la entrega se retrase (DL-40).
- **Arreglo:** convertir PRD-348 en una lista de aceptación: "FR-4, FR-5, FR-6, FR-7, FR-8 completos para el Guinardó A; entrada directa en su resumen; FR-34 sí; FR-32 solo en [idioma]; FR-18, FR-33 [sí/no]; fuera FR-1 a FR-3 y FR-9 a FR-17. Riesgo aceptado: puede no estar el 23/10 porque primero se cierra el PRD (DL-40)". Confirmar con Luis lo que está entre corchetes.

### M-5. A-3 crea una excepción a la anonimización que Luis no planteó
- **Evidencia:** DL-46 "en categorías de menores los jugadores **se muestran anonimizados** […]; las estadísticas se mantienen", sin excepciones.
- **PRD:** FR-17 / A-3 (PRD-226) "los Gestores de un Equipo de menores ven los nombres completos de su propio Equipo". Está etiquetado, pero el valor por defecto propuesto es el más arriesgado, porque cualquiera puede pedir ser Gestor (FR-21) y Q-2 sigue PENDIENTE.
- **Arreglo:** cambiar el valor por defecto de A-3 a "anonimizado también para Gestores en v1" y dejar la excepción como opción que Luis puede activar después de Q-2.

### M-6. El dorsal no es estable ni único: afecta a la anonimización y a la plantilla
- **Evidencia (Dossier, Darna):** "#9 Ali Bouchikhi" y "#9 Youssef Ariri"; "#2 Darboe" y "#2 Brik"; "#6 Joof" y "#6 Mohamed El". En TFC hay tres #9 y dos #23, #15 y #14.
- **PRD:** FR-8 "con dorsal"; FR-17 "iniciales y dorsal". Con dorsales repetidos o que cambian, "D. A. #8" no identifica a nadie de forma estable y dos menores pueden verse iguales.
- **Arreglo:** "El dorsal mostrado es el más frecuente del Jugador en la Temporada. Si dos Jugadores Anonimizados coinciden en iniciales y dorsal, se desambiguan [regla]". Incluirlo en las consecuencias de FR-17.

### M-7. No está claro qué aporta el Dossier frente a las Estadísticas avanzadas públicas
- **Evidencia:** DL-32 abre a todos las estadísticas avanzadas en la Ficha de equipo de **cualquier** Equipo. DL-22 y DL-27 hacen el Dossier privado "para que no llegue al rival".
- **Problema:** con el PRD tal cual, cualquiera (incluido el rival) ve en la Ficha de equipo del Guinardó casi todo lo que contiene un Dossier sobre el Guinardó. La privacidad del Dossier solo protege la *selección* (a quién estoy preparando) y, en el futuro, las Claves. No es un error del PRD, porque Luis decidió ambas cosas, pero el PRD no lo explica, y eso afecta al valor del Hito 2 y a SM-3 (que podría cumplirse ya en el Hito 1).
- **Arreglo:** añadir en §5.11 un párrafo con lo que el Dossier aporta sobre la Ficha de equipo: todo en una vista, comparación con el propio Equipo (M-2), Enlace privado y, después del MVP, Claves. Confirmar con Luis que lo acepta.

### M-8. Métricas con objetivos inventados y una métrica de Luis desplazada al Hito 2
- **Evidencia:** DL-44 "uso semanal por el cuerpo técnico del Guinardó […] ahorro de tiempo […] (de horas a minutos)"; DL-49 "20 seguidores […] en el primer mes".
- **PRD:**
  - SM-1 (PRD-368) "Objetivo: 4 Jornadas seguidas **tras el Hito 2**" y lo liga solo al Dossier. Luis no puso cifra y su métrica de uso semanal también aplica al Hito 1 (calendario, plantilla, ficha del rival).
  - SM-3 "menos de 10 minutos": cifra inventada.
  - SM-2 "tras el Hito 1": ancla supuesta.
  - SM-4 "cero discrepancias": de buen sentido, pero inventada.
- **Arreglo:** etiquetar como `[ASSUMPTION]` las cifras de SM-1, SM-3 y SM-4 y el ancla de SM-2, y añadirlas al índice §10. Añadir una SM-1a de uso semanal del cuerpo técnico desde el Hito 1 (o desde el 23/10).

### M-9. Se presentan como decididos la frontera gratis/de pago y el tipo de proyecto
- **Evidencia:** DL-18 "Tensión abierta […] Hay que fijar la frontera gratis / de pago"; DL-25 "Tensión resuelta […] — fuente: **PM**, a partir de las respuestas" (Luis no la confirmó); DL-13 "Tipo de proyecto (inferido, **a confirmar**)".
- **PRD:** PRD-21 ("cualquier Equipo puede usarla desde el primer día sin alta manual") y PRD-26 ("Tipo de proyecto: MVP de validación…") lo presentan como hecho. En el futuro, "pagar por dar de alta un club con sus estadísticas" (DL-14) implica que el alta, o al menos las estadísticas, de un club podrían dejar de ser gratis, y el PRD no lo dice.
- **Arreglo:** etiquetar ambos como `[ASSUMPTION]` en §10 (A-7, frontera gratis/pago; A-8, tipo de proyecto) para que Luis los confirme. Basta una línea de confirmación.

---

## BAJO

### L-1. El formato de anonimización no coincide con el ejemplo de Luis y no es testable
DL-46 pone el ejemplo **"D. A." #8**; PRD-224 dice "**Q. A. V.** o similar". "O similar" no se puede testear. **Arreglo:** fijar el formato (p. ej. inicial del nombre + inicial del primer apellido + dorsal, "Q. A. #8") y usar un único ejemplo.

### L-2. "Goleadores" en FR-25 es ambiguo
El dossier tiene una sección de grupo "Goles" con el ranking de todo el Grupo y los penaltis ("Franco Acha River Plate · 1 de penalti"). FR-25 dice solo "goleadores". **Arreglo:** "goleadores del rival y ranking de goleadores del Grupo (FR-10), con penaltis".

### L-3. Faltan en el Dossier los totales disciplinarios del rival
Dossier: "La FCF les apunta 3 dobles amarillas"; "13 amarillas en 4 partidos". Están en Claves, pero son datos estructurados (del joc net, FR-11), no narrativa. **Arreglo:** añadir a FR-25 "amarillas, dobles amarillas y rojas del rival en la Temporada".

### L-4. La frase-titular de cada rival también es narrativa
Dossier: "Colista: sin victorias en cuatro partidos, pero marca en todos." / "3 de sus 6 puntos son de despacho." FR-25 solo aplaza las "Claves". **Arreglo:** en "Fuera de alcance" de FR-25 decir "Claves y frase-resumen del rival (IA): post-MVP".

### L-5. Detalles de la tabla de plantilla del dossier no recogidos
La leyenda "T titular · S suplente · – no convocado · **primer partido**" marca el debut de cada jugador en su columna (no solo el del último partido). Las columnas son solo jornadas jugadas (J3 pendiente no aparece) y llevan el escudo del rival de cada jornada, y se muestra "Plantilla 23 jugadores". FR-8 solo destaca "debutante en el último Partido". **Arreglo:** añadir a FR-8 "marca de primer partido en la tabla; columnas = Jornadas jugadas con el rival de cada una; total de Jugadores".

### L-6. Goles sin minuto
En el dossier de Poble Nou los Tramos suman 5 goles en contra, frente a los 6 de campo que da la propia Clave, así que algún gol no tiene minuto en el Acta. FR-14 no dice qué pasa en ese caso. **Arreglo:** "un gol sin minuto cuenta en totales y se muestra como 'sin minuto' fuera de los Tramos". Lo mismo para la regla del añadido (PRD-209), que es del PM: etiquetar o confirmar.

### L-7. Sanciones: falta "¿puede jugar el próximo partido?"
Dossier (Claves propias): "Alarcón Chauca tiene 2 partidos de sanción desde la J4. Cumplió uno en la J5, así que **en principio no puede jugar hoy**". FR-16 da los partidos restantes, pero no la conclusión útil. **Arreglo:** consecuencia en FR-16 y FR-25: "se indica si el Jugador está disponible para el próximo Partido (con 'en principio' si es una deducción)".

### L-8. Detalles inventados por el PM sin etiqueta
Son razonables, pero Luis no los pidió:
- FR-1: mínimo de 3 caracteres; la búsqueda devuelve solo Clubs aunque el FR dice "Club o Equipo".
- FR-2: los Equipos seguidos pasan a la Cuenta al crearla.
- FR-21: "relación declarada" y aviso de cambio de estado de la Solicitud, que es un **quinto tipo de aviso** fuera de la lista de DL-31.
- FR-22: retirar el rol de Gestor.
- FR-28 a FR-31: activar o desactivar cada aviso por Equipo.
- FR-15: 7 en Futbol 7.
- FR-33: amplía la hora de frescura a cambios de Partido y sanciones; DL-47 habla de "resultado o acta".
- PRD-41: el Administrador "modera", cuando no hay contenido de usuarios (non-goal).
- §6: "ni amistosos".
- §7.2: "Temporadas anteriores".

**Arreglo:** etiquetar como `[ASSUMPTION]` en bloque o confirmarlos en una sola ronda con Luis; quitar "modera".

### L-9. UJ-1 probablemente desactualizado
PRD-51: "el último resultado (5-0)". El Guinardó jugaba el aplazado J3 contra Torre Fuerte el lunes 19/10 (Dossier: "Partido aplazado de la J3, hoy lunes 19/10"). El 23-24/10 el último resultado será ese, no el 5-0. **Arreglo:** comprobar en la FCF y actualizar el ejemplo, o redactarlo sin marcador concreto.

### L-10. Marca en el nivel de Club y otros detalles menores
- FR-19 habla de "la Marca de su Equipo", pero existe el Gestor de Club entero (FR-21). Falta decir si puede aplicar una Marca a todos los Equipos del Club.
- No se fija el formato de nombre: FCF da "ARUMÍ VALLALTA, QUIM" y el dossier usa "Quim Arumí Vallalta".
- No se recoge el riesgo de que los planes gratuitos (DL-38) no basten para refrescar cada hora (DL-47) los datos de cualquier club (DL-9).

**Arreglo:** una línea en FR-19, una en el glosario (Jugador: formato de nombre) y una en preguntas abiertas internas.

---

## Comprobaciones superadas (sin hallazgo)

- **Roles:** Seguidor, Gestor y Administrador; el Gestor se solicita y lo aprueba el Administrador (DL-26); Gestor por Equipo o por Club.
- **Disciplinas v1:** F11, F7 y Femení; fuera F5, Sala, Sala Femení y Platja (DL-24).
- **Hitos 1 y 2:** su contenido coincide con DL-35. El Hito 1 añade 5.8 (menores) y 5.13, que son consecuencias directas de DL-46, DL-33 y DL-47.
- **Marca:** FCF automática más ajuste manual del Gestor; la extracción desde redes queda post-MVP (DL-28). En el Feed, colores por tarjeta y Tema completo al entrar en un Equipo (DL-53).
- **Cuenta:** opcional y necesaria para notificaciones y para pedir ser Gestor (DL-30). Las notificaciones son las 4 de DL-31, con la restricción del iPhone.
- **Export:** por Enlace privado, no PDF (DL-52). Las Claves por IA quedan post-MVP (DL-11).
- **Dossier:** de un rival concreto y bajo petición (DL-42, DL-27).
- **Vistas abiertas:** plantilla con matriz, ficha de jugador, rankings (goleadores, joc net, sanciones) y estadísticas avanzadas (DL-32).
- **Idioma:** ca/es, sin traducir los datos de la FCF (DL-33). Frescura máxima de 1 h (DL-47). Tramos: 6 proporcionales (DL-48).
- **Competiciones:** solo liga (DL-43). Los non-goals de DL-54 están todos.
- **Bloques del dossier cubiertos:**
  - clasificación con racha y zonas (FR-6, FR-25);
  - goleadores con penaltis (FR-10);
  - resultados por jornada con aplazados y despacho (FR-5, FR-25);
  - marcó primero (FR-13);
  - tramos de 15' (FR-14);
  - once (FR-15, salvo M-1);
  - matriz T/S/– (FR-8);
  - debutantes (FR-8, FR-25);
  - sanciones y partidos restantes (FR-16);
  - próximo partido con casa o fuera (FR-25).
