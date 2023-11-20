import nuke
import Breakout_Lightgroups

menu = nuke.menu("Nuke")
lola_tools = menu.addMenu("&Lola")
lola_tools.addCommand("lighting/BreakOutLightGroups", "Breakout_Lightgroups.shuffle_out_lightgroups( nuke.selectedNode() )")
