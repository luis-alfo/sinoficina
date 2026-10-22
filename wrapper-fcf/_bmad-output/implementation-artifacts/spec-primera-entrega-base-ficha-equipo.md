---
title: 'Primera entrega: base del proyecto + Ficha de equipo del Guinardó A'
type: 'feature'
created: '2026-10-22'
status: 'draft'
context:
  - '{project-root}/_bmad-output/planning-artifacts/prd-wrapper-fcf/prd.md'
---

<!-- Borrador de discovery (nch-spec step-02). Se reescribe entero en step-03. -->

## Hallazgos validados (ronda 1)

- Proyecto greenfield: no hay código previo de la app. Stack fijado por Luis: React + Supabase + Vercel, PWA.
- Alcance (PRD §7.1, spec 1 de 3): la app abre en la Ficha de equipo del Guinardó A (CODEQUIPO 40574, Grup 20 = CODGRUPO 58161913, temporada 22) con FR-4 Resumen, FR-5 Partidos, FR-6 Clasificación, FR-18 Tema automático, FR-29 ca/es (catalán por defecto), FR-30 frescura ≤ 1 h, FR-32 atribución. Ficha de partido (FR-7) y Plantilla (FR-8) van en las specs 2 y 3 (`deferred-work.md`).
- La API de fcf.cat no devuelve cabeceras CORS: el navegador no puede llamarla desde otro dominio. Hace falta una pieza en servidor que lea la FCF y guarde los datos (además, FR-31 exige servir los últimos datos buenos si la FCF cae).
- Fuentes FCF para esta spec (ver `fcf/ENDPOINTS.md`): `/api/clubs/{club}/team/{equipo}?temporadaId=` (info + matches con CODGRUPO), `/api/competition/partidos?grupId=`, `/api/competition/classificacio?grupId=`, `/api/competition/equipacions?grupId=` (colores; filas duplicadas), escudos en `files.fcf.cat/escudos/clubes/escudos/{escudo}`.
- Estados de Partido observados en `partidos`: `ESTADO/CERRADA` = `0/0` (programado), `1/1` (jugado, Acta cerrada), `3/1` sin goles (pendiente de interpretar). Aplazado no tiene marca propia: el Partido reprogramado conserva su JORNADA con nueva fecha y nuevo CODACTA. Resultado de despacho: resultado oficial ≠ goles del Acta.
- `COMIENZO1` es hora local de Catalunya (en `acta` lleva una `Z` falsa).
- El detalle de equipo trae teléfonos y horarios de entrenamiento: no se muestran (PRD §6).
- Supabase: org "larc stuff", proyectos `habitos` (activo) y `gymtracker` (pausado). Ninguno es de esta app.
