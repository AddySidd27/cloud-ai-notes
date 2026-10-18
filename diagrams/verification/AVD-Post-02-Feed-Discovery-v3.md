# Feed discovery (post 2, figure 2)

Files: `AVD-Post-02-Feed-Discovery-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/feed_v3.py`.
Type: Documented flow

Method and limits: Redrawn on 18 October 2026 from Learn's own picture, viewed in a browser, with the Learn text fetched the same day. Names, links and arrowheads follow the picture. Observations of Learn's pictures are in `learn-diagram-notes.md`. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience), feed-discovery-single-azure-region.png (and the different-geography picture, not reproduced)

## Explanation
How the feed is retrieved in one Azure region, as drawn by Learn.

## Verification checklist (rechecked 18 October 2026 against Learn's own diagrams)
- [x] Region 1 box: Client two-way Web service two-way Resource directory.
- [x] Client dashed two-way link to Azure Traffic Manager, outside Region 1.
- [x] Geographical deployment scope and Regional deployment scope boxes each hold a broker two-way with its database; the scope boxes carry no region label in the single-region picture.
- [x] One line from the Resource directory splits to both brokers, as in the picture.

## Assumptions and design choices (not Learn requirements)
- Layout positions are the author's; relationships follow the picture.

## Unresolved questions for review
- Picture versus text: the picture joins web service to resource directory to brokers; page text step 2 says web service to broker, and step 3 says broker to resource directory and database. Learn's component interconnection picture shows the broker doing that. Flagged in the image and caption, not resolved.
- Whether the Traffic Manager link is meant as a data hop is not stated; it is drawn dashed as Learn draws it.
