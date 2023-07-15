import re
import nuke

# these look repetetive but the important thing is if we need to update in future from say "LGT" to "lgt" then they are all in one place!!
LIGHT_GROUP_REGEX = re.compile(r'(LGT\d+)(_\w+_?\w+)')
LIGHT_GROUP_FLAG_REGEX = re.compile(r'LGT\d+')
LIGHT_GROUP_FLAG = 'LGT'


aovs = [
'diffuse_direct',
'diffuse_indirect',
'reflect_direct',
'reflect_indirect',
'refract_direct',
'refract_indirect',
'sss_direct',
'sss_indirect'
]

def get_layers(thisNode):
    '''returns a list of all the layers '''
    channels = thisNode.channels()
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()
    return layers

def get_aovs_per_lightgroup(node):
    '''Returns a dictionary of lightgroups containing lists of all the aovs under each) '''
    layers =' '.join ( get_layers(node) )
    aovsPerLG = LIGHT_GROUP_REGEX.findall(layers)
    aovsPerLGSorted = {}
    for aov in aovsPerLG:
        lg = aov[0]
        if lg not in aovsPerLGSorted:
            aovsPerLGSorted[aov[0]] = []
    for aov in aovsPerLG:
        aovsPerLGSorted[aov[0]].append(aov[1] )

    return aovsPerLGSorted


def remove_lg_knobs():

    # Get the my_knob and remove button.
    knob_name = nuke.thisKnob().name()[:-7]
    knob_name_remove = nuke.thisKnob()

    # Delete them!
    nuke.thisNode().removeKnob(nuke.thisNode().knob(knob_name))
    nuke.thisNode().removeKnob(knob_name_remove)

    # Dive into the group and find the node with the label that matches the knobs that were
    # just removed. DELETE THE NODE!
    nuke.thisNode().begin()
    for node in nuke.allNodes():
        if knob_name in node.knob('label').value():
            nuke.delete(node)
