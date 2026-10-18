from common3 import *
NAME = "AVD-Post-02-Feed-Discovery-v3"
W, H = 1000, 660
d = D(W, H, "Feed discovery in one Azure region, as drawn on Learn",
 "Not an official Microsoft diagram. It follows the Learn feed discovery diagram for a host pool in a single Azure region. A client and the web service are joined by a two-way arrow, and the web service and the resource directory are joined by a two-way arrow, all inside a box labelled Region 1. A dashed two-way link joins the client and Azure Traffic Manager. Below, a geographical deployment scope box and a regional deployment scope box each hold a broker joined by a two-way arrow to its database. One line leaves the resource directory and splits to the geographical broker and to the regional broker. The page text describes the flow differently: the web service connects to the broker service, which connects to the resource directory and the database.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 36, "Feed discovery in one Azure region", 20, True, "middle", INK)
d.text(500, 58, "Redrawn from the Learn picture. The page text describes it differently, see the note below.", 14, False, "middle", INK)
tbox(d, 24, 110, 130, 100, ["", "Client"], "#ffffff", GREEN, 14, bold_all=True); d.icon(69, 122, 40, "dev")
tbox(d, 24, 330, 130, 110, ["", "Azure Traffic", "Manager"], "#ffffff", BLUE, 14, bold_all=True); d.icon(69, 340, 40, "tm")
d.line(89, 210, 89, 330, GREYL, 2.5, "3,4", True); d.line(89, 330, 89, 210, GREYL, 2.5, "3,4", True)
d.rect(200, 80, 775, 180, "#f3f7fc", GREYL, 1.6, 8)
d.text(587, 102, "Region 1", 14, True, "middle", INK)
tbox(d, 330, 125, 140, 90, ["Web service"], "#ffffff", BLUE, 14, bold_all=True)
tbox(d, 760, 125, 160, 90, ["Resource directory"], "#ffffff", BLUE, 14, bold_all=True)
d.line(154, 170, 330, 170, INK, 2.5, None, True); d.line(330, 170, 154, 170, INK, 2.5, None, True)
d.line(470, 170, 760, 170, INK, 2.5, None, True); d.line(760, 170, 470, 170, INK, 2.5, None, True)
for x, w, t, br, db in [(200, 385, "Geographical deployment scope", "Geographical broker", "Geographical database"),
                        (600, 375, "Regional deployment scope", "Regional broker", "Regional database")]:
    d.rect(x, 300, w, 230, "#ffffff", GREYL, 1.6, 8)
    d.text(x+w/2, 515, t, 14, True, "middle", INK)
    tbox(d, x+20, 370, 140, 80, br.split(" "), "#ffffff", BLUE, 14, bold_all=True)
    d.rect(x+215, 370, 150, 80, "#ffffff", BLUE, 1.2, 6); d.icon(x+223, 392, 36, "sql")
    d.text(x+265, 405, db.split()[0], 13, True, "start", INK); d.text(x+265, 423, "database", 13, True, "start", INK)
    d.line(x+160, 410, x+215, 410, INK, 2.5, None, True); d.line(x+215, 410, x+160, 410, INK, 2.5, None, True)
d.line(840, 215, 840, 280, BLUE, 2.5, None, False)
d.line(840, 280, 290, 280, BLUE, 2.5, None, False)
d.line(290, 280, 290, 370, BLUE, 2.5, None, True)
d.line(690, 280, 690, 370, BLUE, 2.5, None, True)
d.rect(15, 545, 970, 105, "#ffffff", ORANGE, 1.4, 6)
d.text(30, 568, "Flagged difference inside Learn, not resolved here", 14, True, "start", INK)
for i, t in enumerate(["The picture joins the web service to the resource directory and the resource directory to the brokers.",
                       "The page text says the web service connects to the broker service, and the broker connects to the resource",
                       "directory and the database. The component interconnection diagram on the same page shows the broker doing that."]):
    d.text(30, 590+i*20, t, 13, False, "start", INK)
finish3(d, NAME, "avd-post02-feed-v3", "AVD feed discovery on Learn v3")
