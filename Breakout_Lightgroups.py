import re
import nuke
import nukescripts

def deselect_all_nodes():
    for n in nuke.selectedNodes():
        n['selected'].setValue(False)

def get_layers(readNode):
    '''returns a list of all the layers '''
    channels = readNode.channels()
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()
    return layers


def get_lightgroups(node, flags ):
    '''Returns a list of aovs which are lightgroups (based on naming convention flags set in LightGroupLabels list) '''

    lightGroupLayers=[]
    for aov in get_layers(n):

        for flag in flags:
            if flag in aov and aov not in lightGroupLayers:
                lightGroupLayers.append(aov)
    lightGroupLayers.sort()
    return lightGroupLayers

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


def break_out_by_lightgroup(node):
    unpremult=nuke.createNode('Unpremult')
    unpremult['channels'].setValue('all')
    for key in get_aovs_per_lightgroup(node):
        nuke.createNode('NoOp')



def shuffle_out_lightgroups(node, x_space=600, y_space=300, emission=True):
    '''This will create a mini comp from the layers flagged as lightgroups in the user defined settings. Flags, spacing and use of postage stamps can be set in the panel as per the lightgroup_minicomp_settings function() '''

    x_pos, y_pos=int( node.xpos() ), int( node.ypos() )
    y_pos+=y_space
    beautyDot=nuke.nodes.NoOp(label = 'beauty', inputs=[node])
    beautyDot.setXYpos(node.xpos(), y_pos)
    y_pos+=y_space
    unpremult=nuke.nodes.Unpremult(channels='all', inputs=[beautyDot])
    unpremult.setXYpos(node.xpos(), y_pos)
    y_pos +=int(y_space/3)
    remove_rgb=nuke.nodes.Remove(channels='rgb', inputs=[unpremult])
    remove_rgb.setXYpos(node.xpos(), y_pos+(int(y_space/3)))
    y_pos+=y_space


    indexNo =0
    b_pipe_nodes=[remove_rgb] #all the merge nodes will be added to this list
    top_dots = [unpremult]

    for lg in get_aovs_per_lightgroup(node):
        deselect_all_nodes()
        selected=[]
        x_pos +=x_space
        y_pos +=y_space

        dot=nuke.nodes.Dot( inputs=[ top_dots [indexNo] ] )
        top_dots.append(dot)
        dot.setXpos (x_pos)
        dot.setYpos(unpremult.ypos())


        lg_grade=nuke.nodes.LolaLightGroupGrader(label=lg, inputs=[top_dots[indexNo+1]] )


        lg_grade['get_light_groups'].execute()
        lg_grade['lightgroup'].setValue( lg )
        lg_grade['output'].setValue( 'lightgroup graded' )
        #shuffle_node['postage_stamp'].setValue( settings['pstamps'])
        lg_grade.setYpos(dot.ypos()+ 100)
        temp_dot=nuke.nodes.Dot( ) #defines corner of backdrop
        temp_dot.setXpos(x_pos+int(x_space/2))
        temp_dot.setYpos(lg_grade.ypos()+ y_space*3)
        for n in [dot, lg_grade, temp_dot]:
            n['selected'].setValue(True)

        bg = nukescripts.autoBackdrop()
        bg['label'].setValue(lg)

        y_pos +=y_space
        #from_node=nuke.nodes.Merge2 (operation ='from', tile_color='4278190335.0', label = '<i>'+lg, inputs=[ b_pipe_nodes[indexNo], b_pipe_nodes[indexNo] ], Achannels=lg)
        #from_node.setXYpos(node.xpos(), y_pos )
        bottom_corner = nuke.nodes.Dot( inputs=[ lg_grade ], tile_color='536805631.0', label = '<i>'+lg )
        y_pos +=int(y_space/2)


        nuke.delete(temp_dot)
        bottom_corner.setXYpos(x_pos, y_pos )
        merge = nuke.nodes.Merge2 (operation ='plus', label = '<i>'+lg, tile_color='536805631.0', inputs=[ b_pipe_nodes[indexNo], bottom_corner ])
        b_pipe_nodes.append( merge )
        merge.setXYpos(node.xpos(), y_pos)

        indexNo +=1


    if emission:
        deselect_all_nodes()
        x_pos +=x_space
        y_pos +=y_space

        dot=nuke.nodes.Dot( inputs=[ top_dots [indexNo] ] )
        top_dots.append(dot)
        dot.setXpos (x_pos)
        dot.setYpos(unpremult.ypos())
        shuffle_node = nuke.nodes.Shuffle2( label='emission', inputs=[top_dots[indexNo+1]] )
        shuffle_node['in1'].setValue('emission' )
        #shuffle_node['postage_stamp'].setValue( settings['pstamps'])
        shuffle_node.setYpos(dot.ypos()+ 100)
        exposure_node=nuke.nodes.EXPTool( label='emission', inputs=[shuffle_node] )
        multiply_node=nuke.nodes.Multiply( label='emission', inputs=[exposure_node] )
        multiply_node['channels'].setValue('rbg')
        temp_dot=nuke.nodes.Dot( ) #defines corner of backdrop
        temp_dot.setXpos(x_pos+int(x_space/2))
        temp_dot.setYpos(shuffle_node.ypos()+ y_space*3)
        y_pos +=y_space
        #from_node=nuke.nodes.Merge2 (operation ='from', tile_color='4278190335.0', label = '<i>'+lg, inputs=[ b_pipe_nodes[indexNo], b_pipe_nodes[indexNo] ], Achannels=lg)
        #from_node.setXYpos(node.xpos(), y_pos )
        bottom_corner = nuke.nodes.Dot( inputs=[ shuffle_node ], tile_color='536805631.0', label = '<i>'+lg )
        y_pos +=int(y_space/2)
        bottom_corner.setXYpos(x_pos, y_pos )
        merge = nuke.nodes.Merge2 (operation ='plus', label = '<i>'+lg, tile_color='536805631.0', inputs=[ b_pipe_nodes[indexNo], bottom_corner ])
        b_pipe_nodes.append( merge )
        merge.setXYpos(node.xpos(), y_pos)
        for n in [dot, shuffle_node, temp_dot]:
            n['selected'].setValue(True)
        bg = nukescripts.autoBackdrop()
        bg['label'].setValue('emission')
        nuke.delete(temp_dot)

        indexNo +=1

    y_pos +=y_space
    alpha_dot = nuke.nodes.Dot(inputs = [beautyDot])
    alpha_dot2 = nuke.nodes.Dot(inputs = [alpha_dot])
    alpha_dot.setXYpos(unpremult.xpos()-int(x_space/2), beautyDot.ypos() )
    alpha_dot2.setXYpos(alpha_dot.xpos(), y_pos )
    copy_alpha = nuke.nodes.Copy(from0 = 'rgba.alpha', to0 = 'rgba.alpha', inputs = [merge, alpha_dot2] )
    copy_alpha.setXYpos(node.xpos(), y_pos )
    y_pos+=y_space
    remove_node=nuke.nodes.Remove(inputs = [copy_alpha], operation='keep', channels='rgba', label ='<b>[value operation] [value channels]')
    remove_node.setXYpos(node.xpos(), y_pos)
    y_pos+=y_space
    premult = nuke.nodes.Premult(inputs = [remove_node] )
    premult.setXYpos(node.xpos(), y_pos)
