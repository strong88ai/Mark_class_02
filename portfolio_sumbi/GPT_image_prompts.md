# 숨비 포트폴리오 — GPT 이미지 프롬프트 (도면 기준)

## 사용법 (모든 프롬프트 공통)
1. **새 대화창**을 열고, 아래 `첨부`에 적힌 이미지를 **먼저 올린 뒤** 프롬프트를 붙여넣습니다.
   - 도면 이미지: `gpt_reference/plan_B1.jpg`, `plan_1F.jpg`, `plan_2F.jpg`
   - 렌더 이미지: 직접 만든 아이소메트릭·탑뷰 렌더, 현장 모델 항공샷
2. 결과가 틀리면 **같은 대화창**에서 `확인`에 적힌 항목 중 틀린 것만 짧게 고쳐 달라고 요청합니다. 새로 생성하는 것보다 정확합니다.
3. 글자·라벨은 넣지 않습니다. 라벨은 포트폴리오 파일에서 벡터로 얹습니다.

### 이 집의 기준 정보 (모든 프롬프트에 반영됨)
| 층 | 크기 (mm) | 주요 실 | 층고 (가정) |
|---|---|---|---|
| B1 | 24,500 × 18,600 | 현관, 주차장 4대, 거실(라운지), 수영장, 바이크 창고, 캠핑 창고, 드레스룸, 보일러·기계실, 세탁실, 샤워실, 외부 계단 출입구 | 4.2m |
| 1F | 21,200 × 18,600 | 주방, 팬트리, 거실·다이닝, 게스트룸, 화장실, 테라스, 마당, 외부 계단 | 3.6m |
| 2F | 18,850 × 17,500 | 침실, 안방, 거실, 드레스룸, 화장실 3, 세탁실, 곡선 테라스, 자쿠지(사다리꼴) | 3.6m |

- 대지: 해안도로 → 야자수 광장(평탄) → 집 → 바위 호안 → 바다(남쪽)
- 1F 바닥 = 광장·도로 높이. B1은 완전히 땅속. 해수면은 광장보다 약 3m 아래(가정).

---

## ① 3p 대지 분석 — 대지 배치 입체도
**첨부:** 현장 모델 항공샷 2장, `plan_1F.jpg`
**비율:** 정사각형 1024×1024

```
Use the attached aerial screenshots as the exact site layout reference and the attached floor plan for the house footprint. Create a clean architectural site analysis axonometric diagram of this coastal site in Jeju, South Korea.

CAMERA: high bird's-eye axonometric view from the south-west, looking north-east, 40-degree downward angle, no perspective distortion. North is toward the top of the image, the sea is at the bottom.

SITE LAYOUT — keep this exact order from bottom to top:
1. Bottom: calm open sea, flat muted blue-gray (#5E7480), subtle horizontal ripple lines only.
2. A continuous seawall of large stacked dark basalt boulders (riprap) running along the whole shoreline, dropping about 3 m from the plaza level down to the water.
3. The site band: a long FLAT coastal plaza paved in light sand-colored stone slabs, with two straight rows of small palm trees and a dark-brown paved walkway running parallel to the shore, plus one short dark walkway connecting the plaza to the road.
4. The house sits at one end of the plaza, directly next to the boulder seawall:
   - a modern white flat-roof house, two storeys above ground (ground floor 1F + upper floor 2F), footprint about 21 m x 19 m;
   - ground floor: glass folding doors opening south onto a stone terrace and a green lawn yard that reaches the seawall;
   - upper floor: an L-shaped volume on the north and west sides, with a large CURVED terrace with a low glass railing on the south-east, ending in a small trapezoid-shaped jacuzzi that points toward the sea;
   - a small stair/elevator box on the roof;
   - an exterior stair on the east side going down to a basement entrance (the basement itself is underground and not visible).
5. Next to the house on the other side: a neighboring white building with a smooth curved shell-shaped roof and a glass facade, with its own small garden.
6. Above the plaza: a straight two-lane coastal road with a single solid yellow center line.
7. Top of image: a row of simple 2–3 storey houses across the road, shown as plain white massing blocks without detail.

STYLE: competition-board white-model style. Only the house has real materials (white lime plaster walls, warm oak, dark basalt base, green roof plants, the turquoise jacuzzi water); everything else is simplified white or light-gray massing so the house stands out. Soft daylight coming from the bottom (south), soft shadows falling toward the top (north). Background outside the site: warm beige (#F2EEE8). Muted palette: basalt charcoal #2B2B2B, volcanic red-brown #7A4A3A (tiny accents only), sand #E8E1D6, sea #5E7480.

DO NOT include: any text, labels, numbers, arrows, compass, people, cars, boats, logos or watermark.
```
**확인:** 집이 호안 바로 옆인가 / 지상 2개 층인가 / 2층 곡선 테라스 끝에 자쿠지가 있는가 / 도로 중앙선이 노란 실선인가 / 바다가 아래쪽인가

---

## ② 3p 위치도 — 제주와 대포동
**첨부:** 없음 (또는 제주 지도 캡처)
**비율:** 가로 1536×1024

```
Minimal flat vector-style location map of Jeju Island, South Korea, seen from directly above, north up.

ISLAND: accurate oval silhouette of Jeju Island, wider east–west than north–south (about 73 km x 31 km), filled with light warm gray (#D8D1C6). A very subtle set of 3–4 concentric contour lines around Hallasan mountain at the center of the island, slightly darker gray, thin lines.
MARKER: one small red-brown dot (#7A4A3A) with a thin ring around it, placed on the SOUTH coast of the island, slightly WEST of the center (the Jungmun / Daepo area of Seogwipo), sitting exactly on the coastline.
SEA: the surrounding sea in flat muted blue-gray (#5E7480) at 30% opacity, fading to the beige background (#F2EEE8) at the image edges.

STYLE: clean, flat, minimal, generous empty margins, island occupies about 70% of the image width.
DO NOT include: text, labels, roads, city icons, gradients on the island, 3D effects, compass, scale bar, watermark.
```
**확인:** 섬이 가로로 긴 타원인가 / 점이 남쪽 해안, 중앙보다 약간 서쪽인가

---

## ③ 4p 단면 투시도 (이전 이미지 대체)
**첨부:** `plan_B1.jpg`, `plan_1F.jpg`, `plan_2F.jpg`, 2F 아이소메트릭 렌더
**비율:** 가로 1536×1024

```
Use the three attached floor plans (B1, 1F, 2F) as the exact layout reference. Create an architectural SECTION PERSPECTIVE (cut-away section render) of this coastal house in Jeju, cut north–south, viewed straight from the side. North (land) on the LEFT, the sea on the RIGHT.

GROUND LINE: a single flat ground line runs across the whole image at the level of the ground floor (1F). To the left of the house is a flat paved coastal plaza and road at exactly this level. Everything below this line is earth, shown as a flat light-beige cut face with thin dark outlines.

THE HOUSE — exactly 3 levels, stacked like this:
1. B1 (basement, FULLY UNDERGROUND, below the ground line, tallest floor ~4.2 m): the full footprint, 18.6 m deep. Contains, from left to right: a car parking garage with two cars, a lounge with a curved sofa, and an indoor swimming pool with warm underwater light on the sea side. NO windows to the sea — the basement is completely buried; daylight reaches the pool only from ABOVE through a long opening/skylight in the ground floor. The concrete walls and floor of the basement are shown thick, with a thin blue waterproofing line wrapping the outside.
2. 1F (ground floor, ~3.6 m, sitting ON the ground line): the enclosed part is on the north/left, about 10.5 m deep: kitchen with an island and a living/dining room with a long table. On the south/right side, full-height glass folding doors open onto a stone terrace and then a green lawn yard that extends to the seawall.
3. 2F (upper floor, ~3.6 m): the enclosed part is on the north/left, only about 7.6 m deep: a living room and dressing room. To the south/right of it a large terrace slab with a low frameless glass railing extends out over the 1F terrace (supported by two slim white columns), and at its seaward end a small SUNKEN JACUZZI with glowing turquoise water, its edge facing the horizon.
4. On the roof: a small box for the stair/elevator core, the rest of the roof flat.

SEA SIDE (right): directly at the end of the lawn, a steep seawall of large dark basalt boulders (riprap) drops about 3 m down to a calm sea. The sea surface is clearly BELOW the ground line and higher than the basement floor, so the basement sits below sea level behind the seawall.

LIGHT AND MOOD: golden-hour sun from the right (sea side), warm interior lights glowing on every floor, soft long shadows. 
STYLE: clean architectural visualization, orthographic-like, no perspective distortion, white lime-plaster walls, warm oak floors, dark basalt base, muted palette (beige background #F2EEE8, basalt charcoal #2B2B2B, volcanic red-brown #7A4A3A accents, sea blue-gray #5E7480).
DO NOT include: text, labels, dimension lines, arrows, people, watermark. Do NOT add any extra floors.
```
**확인:** 지면선 = 1층 바닥인가 / 지하는 1개 층이고 바다 쪽 창이 없는가 / 지상은 2개 층인가 / 자쿠지가 2층 테라스 끝인가 / 1층 남쪽에 마당이 있는가 / 해수면이 지면보다 낮은가

**자주 틀리는 부분 수정 요청 (같은 대화창):**
```
Keep everything else the same. Fix: the ground line must be at the level of the ground floor (1F); there must be only ONE basement level (fully underground, no sea-facing window) and TWO floors above ground. Move the jacuzzi to the end of the upper-floor (2F) terrace.
```

---

## ④ 10p 지하 외벽 레이어 입체도 (받아온 이미지 수정)
**같은 대화창에서:**
```
Keep everything exactly the same, only fix two things:
1. The steel rebar must be embedded INSIDE the concrete wall, not on its surface. Show the cut face of the concrete wall revealing two layers of vertical and horizontal rebar (double reinforcement) inside the concrete, near each face, with concrete cover.
2. Replace the grass on top of the soil with light sand-colored stone paving slabs (a paved plaza surface).
Same camera angle, same lighting, same colors, no text.
```

---

## ⑤ 14p 2F 오션 자쿠지 분위기 컷 (클라이맥스)
**첨부:** `plan_2F.jpg`, 2F 아이소메트릭 렌더
**비율:** 가로 1536×1024

```
Use the attached 2F floor plan and render as the layout reference: the jacuzzi is the trapezoid-shaped pool at the south-east end of the large curved terrace on the upper floor (2F).

Create a photorealistic architectural render of this jacuzzi at dusk.
CAMERA: standing on the curved terrace near the folding glass doors of the 2F living room, eye height 1.5 m, 24 mm lens, looking south-east toward the jacuzzi and the sea.
JACUZZI: a sunken trapezoid-shaped pool whose narrow end points toward the sea; three wide steps on the near side descend into the water; finished inside with dark honed basalt stone tiles; the far (seaward) edge is an INFINITY EDGE so the water surface visually merges with the sea horizon; warm underwater light, gentle steam rising.
TERRACE: warm oak decking around the jacuzzi with a hidden LED strip under the deck edge; the curved terrace edge is lined with a low frameless glass railing; on one side the white lime-plaster wall of the house curves away.
VIEW: beyond the glass, the tops of large dark basalt seawall boulders far below, then the calm open sea and a soft orange-to-lilac twilight sky; the horizon line sits exactly at the water level of the jacuzzi.
MOOD: calm, quiet, meditative, high-end but minimal; no furniture other than two simple towels on the deck.
PALETTE: basalt charcoal, warm oak, white lime plaster, sea blue-gray, a touch of volcanic red-brown.
DO NOT include: people, text, logos, watermark, palm trees inside the frame, extra buildings.
```
**확인:** 자쿠지가 사다리꼴인가 / 계단 3단이 앞쪽에 있는가 / 수면이 수평선과 이어지는가 / 2층 높이에서 바위 호안이 아래로 보이는가

---

## ⑥ 5p B1 아이소메트릭 (임시 이미지 대체)
**첨부:** `plan_B1.jpg`, B1 탑뷰 렌더, 1F 아이소메트릭 렌더(스타일·각도 기준)
**비율:** 정사각형 1024×1024

```
Use the attached B1 floor plan and B1 top-view render as the exact layout reference, and the attached 1F isometric render as the exact STYLE and CAMERA ANGLE reference.

Create a cut-away isometric render of the B1 (basement) floor with no ceiling, walls cut at about 1.2 m height, matching the 1F isometric render's camera angle, lighting, wall cut style and material look exactly, so the two images can be stacked.
LAYOUT (24.5 m x 18.6 m, keep exactly as the plan): boiler & mechanical room (top-left), elevator, stair hall, laundry, shower room, lounge with a curved white sofa, dressing room, camping storage, entrance hall, exterior stair and entrance (top-right), parking garage with four cars (right-center), indoor swimming pool with two lounge chairs (bottom-left), bathroom (bottom-center), bike storage with six motorcycles in a row and a tire rack (bottom-right).
MATERIALS: light gray wood floors in living areas, dark gray stone tiles in bathrooms and pool deck, light patterned stone in the garage, white walls.
BACKGROUND: flat warm beige (#F2EEE8), no ground plane, soft contact shadow.
DO NOT include: text, labels, numbers, people, watermark.
```
**확인:** 각도가 1F 아이소와 같은가 / 실 배치가 도면과 같은가 (특히 주차장 4대, 수영장 좌하단, 바이크 우하단)

---

## 이미지를 받으면 할 일
- 받은 이미지를 보내주시면 해당 페이지에 넣고 라벨을 벡터로 얹습니다.
- 포트폴리오에는 AI 생성 이미지라고 작게 표기합니다.
