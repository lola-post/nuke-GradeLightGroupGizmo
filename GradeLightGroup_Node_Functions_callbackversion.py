import re
import nuke

def get_layers(thisNode):
    '''returns a list of all the layers '''
    channels = thisNode.channels()
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()
    return layers

def get_aovs_per_lightgroup(node):
    '''Returns a dictionary of lightgroups containing lists of all the aovs under each) '''

    lightGroupRegex = re.compile(r'(lgt\d+)(_\w+_?\w+)')
    layers =' '.join ( get_layers(node) )
    aovsPerLG = lightGroupRegex.findall(layers)
    aovsPerLGSorted = {}
    for aov in aovsPerLG:
        lg = aov[0]
        if lg not in aovsPerLGSorted:
            aovsPerLGSorted[aov[0]] = []
    for aov in aovsPerLG:
        aovsPerLGSorted[aov[0]].append(aov[1] )

    return aovsPerLGSorted

callback='''
node = nuke.thisNode()
k=nuke.thisKnob()
if k.name() == 'lightgroup':
    import re
    lg = k.value()
    lgRegex=re.compile(r'lg\d+')
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

    def update_aov_names():
        """
        Will update all the Shuffles, ShuffleCopys and Merge/From nodes to the correct lightgroup
        Will look for knobtypes ['in1','in2','out1','out2','Achannels','Bchannels'] within ['Merge2','Shuffle2','Shuffle','ShuffleCopy','ChannelMerge'] to update
        """
        lgRegex=re.compile(r'lgt\d+')
        knobTypes=['in1','in2','out1','out2','Achannels','Bchannels']
        with node:
            message=''
            for innerNode in nuke.allNodes():
                if innerNode.Class() in ['Merge2','Shuffle2','Shuffle','ShuffleCopy','ChannelMerge']:
                    for knob in innerNode.knobs():
                        if knob in knobTypes:
                            oldLayer=innerNode[knob].value()
                            newLayer=re.sub(lgRegex, lg, oldLayer)
                            innerNode[knob].setValue(newLayer)
    update_aov_names()
    print ('Updated Callback')
'''

#callback='GradeLightGroup_Node.grade_lg_node_callback()'


#node = nuke.thisNode()

#LGdropDownItems=list ( get_aovs_per_lightgroup(node).keys() )
#node['lightgroup'].setValues(LGdropDownItems)
