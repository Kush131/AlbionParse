"""
Albion Online Parsing

This script is used for parsing out Albion Online data.
Maybe it will do more one day? Who knows!

Script assumes you're on a Mac! Change constants to reflect your specific OS.

"""

import os
import xml.etree.ElementTree as ET

import numpy as np

import plotly as plotly
import plotly.graph_objs as go
import plotly.offline as offline

plotly.offline.init_notebook_mode()


GAME_DATA_PATH = "/Applications/Albion-Online.app/Contents/game/Albion-Online.app/Contents/" + \
                    "Resources/Data/StreamingAssets/GameData"

CLUSTERS_PATH = GAME_DATA_PATH + "/cluster"
TEMPLATE_PATH = GAME_DATA_PATH + "/templates"

def grab_xml_filenames():
    """
    Finds all the xml files and formats them with full paths
    """

    game_data = []
    for directory_file in os.listdir(GAME_DATA_PATH):
        if directory_file.endswith(".xml"):
            game_data.append(directory_file)

    clusters = []
    for directory_file in os.listdir(CLUSTERS_PATH):
        if directory_file.endswith(".xml"):
            clusters.append(directory_file)

    return (game_data, clusters)

def grab_xml_fullpath_filenames(game_data, clusters):
    """
    Finds all the xml files and formats them with full paths
    """

    for directory_file in os.listdir(GAME_DATA_PATH):
        if directory_file.endswith(".xml"):
            game_data.append(GAME_DATA_PATH + "/" + directory_file)

    for directory_file in os.listdir(CLUSTERS_PATH):
        if directory_file.endswith(".xml"):
            clusters.append(CLUSTERS_PATH + "/" + directory_file)

def parse_template_resources(template, displayname, results, html_results, html):
    """
    Test out the parsing library on Parchthroat Plain
    """

    tree = ET.parse(TEMPLATE_PATH + "/" + template)
    root = tree.getroot()
    results[displayname] = {}
    for child in root[1]:
        for resource in child.findall('resourcenode'):
            if child.attrib['name'] not in results[displayname]:
                results[displayname][child.attrib['name']] = [child.attrib["pos"]]
            else:
                results[displayname][child.attrib['name']].append(child.attrib["pos"])

    if len(results[displayname]) > 2:
        if html:
            # Format beginning of HTML string.
            html_results += str(displayname) + "<br>----------------------------"
        for resource in results[displayname]:
            if html:
                # Format with <br> for HTML line breaks.
                html_results += "<br>" + str(resource) + \
                ":    " + str(len(results[displayname][resource]))
        if html:
            # End of each template with HTML line breaks.
            html_results += "<br>----------------------------<br>"

    return (results, html_results)

def displayname_to_cluster(d2c_dictionary, c2d_dictionary):
    """
    Creates an association between a display name and its cluster from world.xml
    """

    world_xml_fullpath = CLUSTERS_PATH + "/" + "world.xml"
    tree = ET.parse(world_xml_fullpath)
    for child in tree.getroot()[0]: # Clusters are 0 index.
        if child.attrib['displayname'] is not None:
            d2c_dictionary[child.attrib['displayname']] = child.attrib['file']
            c2d_dictionary[child.attrib['file']] = child.attrib['displayname']

def cluster_to_template(cluster_xml, c2t_dictionary, t2c_dictionary):
    """ Creates an association between a cluster and its template """

    for cluster in cluster_xml:
        tree = ET.parse(CLUSTERS_PATH + "/" + cluster)
        for child in tree.getroot():
            if 'id' in child.attrib:
                if child.attrib['id'] == 'instanceslot_00':
                    c2t_dictionary[cluster] = child.attrib['ref'] + ".template.xml"
                    t2c_dictionary[child.attrib['ref'] + ".template.xml"] = cluster

def test_run():
    '''
    Test run of script
    '''

    d2c = {} # Displayname to Cluster
    c2d = {} # Cluster to Displayname
    c2t = {} # Cluster to Template
    t2c = {} # Template to Cluster
    resource_positions = {} # Positions of all the resources
    html_results_string = "" # Results to print to flask webpage.

    # Add a title to our tab.
    html_results_string += "<head><title>Albion Resource Count</title></head><br>"

    game_data_xml_filenames, cluster_data_xml_filenames = grab_xml_filenames()
    displayname_to_cluster(d2c, c2d)
    cluster_to_template(cluster_data_xml_filenames, c2t, t2c)
    for entry in d2c:
        results, html_results_string = parse_template_resources(c2t[d2c[entry]], entry,
                                                                resource_positions,
                                                                html_results_string,
                                                                True)

    resources = {} # Dict of all resources position data

    for displayname in d2c:
        if 'ORE_HIGH_NODE' in results[displayname]:
            resources['ORE_HIGH_NODE'] = []
            x_position = []
            y_position = []
            z_position = []
            for resource in results[displayname]['ORE_HIGH_NODE']:
                resource_list = resource.split()
                x_position.append(int(resource_list[0]))
                z_position.append(int(resource_list[1]))
                y_position.append(int(resource_list[2]))
            trace1 = go.Scatter3d(
                x=np.asarray(x_position),
                y=np.asarray(y_position),
                z=np.asarray(z_position),
                mode='markers',
                marker=dict(size=12, line=dict(color='rgb(228, 26, 28)', width=0.5),
                            opacity=0.8))

        if 'ORE_MEDIUM_NODE' in results[displayname]:
            resources['ORE_MEDIUM_NODE'] = []
            x_position = []
            y_position = []
            z_position = []
            for resource in results[displayname]['ORE_MEDIUM_NODE']:
                resource_list = resource.split()
                x_position.append(int(resource_list[0]))
                z_position.append(int(resource_list[1]))
                y_position.append(int(resource_list[2]))
            trace2 = go.Scatter3d(
                x=np.asarray(x_position),
                y=np.asarray(y_position),
                z=np.asarray(z_position),
                mode='markers',
                marker=dict(size=12, line=dict(color='rgb(55, 126, 184)', width=0.5),
                            opacity=0.8))

        if 'ORE_LOW_NODE' in results[displayname]:
            resources['ORE_LOW_NODE'] = []
            x_position = []
            y_position = []
            z_position = []
            for resource in results[displayname]['ORE_LOW_NODE']:
                resource_list = resource.split()
                x_position.append(int(resource_list[0]))
                z_position.append(int(resource_list[1]))
                y_position.append(int(resource_list[2]))
            trace3 = go.Scatter3d(
                x=np.asarray(x_position),
                y=np.asarray(y_position),
                z=np.asarray(z_position),
                mode='markers',
                marker=dict(size=12, line=dict(color='rgb(77, 175, 74)', width=0.5),
                            opacity=0.8))

            data = [trace1, trace2, trace3]
            layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
            fig = go.Figure(data=data, layout=layout)
            offline.plot(fig, filename=displayname)

    return html_results_string

test_run()
