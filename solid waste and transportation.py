{
  "nbformat": 4,
  "nbformat_minor": 1,
  "cells": [
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "7255580f-0714-4edd-9aa9-8989ccb2ea9c",
        "collapsed": true,
        "_uuid": "d2a64bbaf584d18c9192d3811209c6b2429b2ddc"
      },
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "%matplotlib inline"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "6b732791-25b2-4282-af0d-93d441547131",
        "_uuid": "c42fddb853067084b058c5750b53341fcc4d6624"
      },
      "cell_type": "markdown",
      "source": [
        "### Read in the data and take a peek"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "b84f37c3-413b-49bb-baef-1683cbbcf42c",
        "_uuid": "adc280a106a9cd7b28118f72e02260af4fed7262"
      },
      "source": [
        "data = pd.read_csv('../input/austin_waste_and_diversion.csv', parse_dates=[2, 5])\n",
        "data.head()"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "8f357ab1-0d9c-411e-a7a3-08590c0a0286",
        "_uuid": "07a61fb7488af5c6595a69110cb89a7779e34573"
      },
      "cell_type": "markdown",
      "source": [
        "Dropping the `report_date` column because in some cases it lags behind the `load_time` by one or more days. Perhaps this is because loads after 5PM don't actually get reported until the next business day? What about the ones that lag by many days...weekends maybe? Special events? Are some type of loads staged until there's enough to deliver?\n",
        "\n",
        "In any case it's not a useful field so I'm dropping it for now."
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "e50e8ad9-d647-4a9a-b3f6-4413937cdae5",
        "collapsed": true,
        "_uuid": "2e9186051550e0d3f789ccda8c86f203e6617b76"
      },
      "source": [
        "data.drop('report_date', axis=1, inplace=True)"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "966c8cd1-442e-4087-a684-00e7401cea30",
        "_uuid": "16ea2918e56e610eee2761129e3146a2371725ef"
      },
      "cell_type": "markdown",
      "source": [
        "## Let's look at the number of each type of collection for the dataset\n",
        "*keep in mind we are only looking at the count for now, not the actual weight*"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "b2cbf2a8-8960-435c-b6fb-cf9e1ca7e1ae",
        "_uuid": "23dd7e71455038ba0b55806f1c2eb016fffec571"
      },
      "source": [
        "plt.figure(figsize=(12,6))\n",
        "load_type_counts = data['load_type'].value_counts()\n",
        "ax1 = load_type_counts.plot(kind='bar');#, logy=True);\n",
        "labels = []\n",
        "for i, label in enumerate(load_type_counts.index):\n",
        "    labels.append('{} - ({})'.format(label, load_type_counts[label]))\n",
        "ax1.set_xticklabels(labels);"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "533dec14-697f-49d4-8e89-580c8e10a768",
        "_uuid": "44576216cec2193d5b0609f5e27efa64355e8cc6"
      },
      "cell_type": "markdown",
      "source": [
        "### Because I live in Austin, I know a little bit about this:\n",
        "* Garbage is picked up every week\n",
        "* Recycling is picked up every two weeks\n",
        "* Residential streets are swept six times per year\n",
        "* Major streets are swept twelve times per year\n",
        "* Yard trimmings are collected weekly\n",
        "* Brush and Bulk are collected twice per year \n",
        "    * There are 10 residential areas (I think) that rotate year-round\n",
        "* Not sure about the paper and comingle recycling\n",
        "    * Maybe this is like bulk pickup for industry?\n",
        "    * Could there have been a change in the collection process? \n",
        "        * *foreshadowing intensifies*\n",
        " \n",
        "The rest are probably not on a schedule (as needed)"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "c2a6ae6d-68c6-432b-82f2-133d3e0c107c",
        "_uuid": "b0e19c351a3e614fd303e4b50d7863379b89c291"
      },
      "cell_type": "markdown",
      "source": [
        "### Comment on `load_type` vs `route_type`\n",
        "It seems that all load types receive waste from several different route types. Also, waste from different route types do not exclusively go to any particular load type. Just thought this was interesting, not sure if anything will come of it.\n",
        "\n",
        "To look at the full list of load type contributions, run this code block:  \n",
        "\n",
        "```python\n",
        "load_by_route_type = data.groupby('load_type')['route_type'].unique()\n",
        "for i in load_by_route_type.index:\n",
        "    print('\\n{}: '.format(i))\n",
        "    for j in load_by_route_type[i]:\n",
        "        print('\\t{}'.format(j))\n",
        "```"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "581dbb0c-2c27-4466-b1ce-71b86d7d99ea",
        "_uuid": "cd335be54c6e0f3343323df36521a8de8bb6c601"
      },
      "cell_type": "markdown",
      "source": [
        "## Now let's look at the waste destinations"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "2b6010e4-fd3f-402d-b693-04ef0109bf4c",
        "_uuid": "fbdde7d603ac8ee5f15286c540f95096f0a7002c"
      },
      "source": [
        "plt.figure(figsize=(12, 6))\n",
        "dropoff_site_counts = data['dropoff_site'].value_counts()\n",
        "ax2 = dropoff_site_counts.plot(kind='bar');\n",
        "labels = []\n",
        "for i, label in enumerate(dropoff_site_counts.index):\n",
        "    labels.append('{} - ({})'.format(label, dropoff_site_counts[label]))\n",
        "ax2.set_xticklabels(labels);"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "f830e930-1b08-497a-bf18-85315173598c",
        "_uuid": "a99a0b762f2650dd14ee2b4628ed049b27864602"
      },
      "cell_type": "markdown",
      "source": [
        "### About some of the waste destinations\n",
        "TDS - Texas Disposal Systems  \n",
        "MRF - Materials Recovery Facility  \n",
        "* TDS Landfill is the primary city dump\n",
        "* I think MRF and TDS MRF are the same recycling facility\n",
        "* Hornsby Bend is a bird observatory/water treatment plant\n",
        "    * This is where Austin's \"Dillo Dirt\" is made\n",
        "* Onion Creek is the Austin Community Landfill\n",
        "* Steiner Landfill is the Creedmore Sanitary Landfill (no organic waste)"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "2b4ae570-c46e-4e56-b3c6-cc8ac6857dd0",
        "_uuid": "76ab16299f17b8d82e5f4588810faf55118e62c3"
      },
      "cell_type": "markdown",
      "source": [
        "### Each one of these takes different streams of waste\n",
        "To see the full list of waste streams to each site run this:  \n",
        "```python\n",
        "dropoff_site_load_types = data.groupby('dropoff_site')['load_type'].unique()\n",
        "for i in dropoff_site_load_types.index:\n",
        "    print('\\n{}: '.format(i))\n",
        "    for j in dropoff_site_load_types[i]:\n",
        "        print('\\t{}'.format(j))\n",
        "```"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "6369cb3a-d61c-4689-8b43-adbe6d5a638e",
        "_uuid": "d1b4f9f1a594acb245c3020d425317bf9193ab5d"
      },
      "cell_type": "markdown",
      "source": [
        "## Check on missing load weights"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "62272001-c419-45df-81dd-0b8e7120f70a",
        "_uuid": "fc8632f5277e16ccd5322297bffb3efec35bc146"
      },
      "source": [
        "missing = data[data['load_weight'].isnull()]\n",
        "missing_perc = len(missing) / len(data) * 100\n",
        "print('Missing Total: {}\\nMissing Percentage: {:.2f}%'.format(len(missing), missing_perc))"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "ae45ea4a-e9a0-48ea-89b5-c1764789c7ab",
        "_uuid": "d403c47cdfb949e79a5b70cee2ebb4d896df0488"
      },
      "cell_type": "markdown",
      "source": [
        "So >10% of the full dataset is missing the weight, let's dig a little deeper"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "5adfc78a-898b-410c-adfd-b3a2ccc9c4ec",
        "_uuid": "bfd49f9a8727c41ce631e8b46f1047b2887110bf"
      },
      "source": [
        "missing['load_type'].value_counts()"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "04f1bff2-3351-4f08-b888-d4c6c7e5da7b",
        "collapsed": true,
        "_uuid": "bb7dc8a39033e0b84e7372b8491556be86ba3b58"
      },
      "cell_type": "markdown",
      "source": [
        "That makes me feel a bit better, most of the missing data is from street sweepers...maybe they don't have to fill out paperwork in some cases? Earlier we saw that there were 72,377 data points for street sweeping, ~82% of which are missing.  \n",
        "\n",
        "Luckily, a very small portion of the rest of the data is missing. For now we'll keep these in but we will need to either fill them in with mean/median or remove them if we want to make predictions in the future"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "3bde6dc4-2d5a-49a4-9624-496f68611617",
        "_uuid": "5f08f5d4bcbb1c68182f3f10a0e0ba9cd1361126"
      },
      "cell_type": "markdown",
      "source": [
        "## Let's see the summary of load weights by load type\n",
        "We'll do this by looking at the description and boxplot"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "5e5761cc-2b0e-42d0-9c5d-d0b8fd66b434",
        "_uuid": "9ff726837b45c6f297fcad7df78a5eaa6eb1306e"
      },
      "source": [
        "ax3 = data.boxplot(by='load_type', column='load_weight', figsize=(12, 6))\n",
        "ax3.set_ylim(-1000,40000);\n",
        "ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90);\n",
        "data.groupby('load_type')['load_weight'].describe()"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "3f8288f8-8b5b-4dcb-a491-593c2f694e98",
        "_uuid": "16694977088fd80471c76c8f1a873f41c6dc3a07"
      },
      "cell_type": "markdown",
      "source": [
        "Two irrelevant but interesting things to note about this dataset:\n",
        "1. There is a single negative value in single-stream recycling\n",
        "    * Was there a pickup of nonrecyclable items from the recycling plant?\n",
        "    * Was this just a typo?\n",
        "2. Imagine a single truck filled with 14,540 lbs of dead animals...YUCK!\n",
        "    * I'm assuming this is in lbs as opposed to kg"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "904b4a54-1974-4857-b5f0-a750de538b2b",
        "_uuid": "ff4f65346ddf25cf3d6ab8f38c9f35bb04c4f7fc"
      },
      "cell_type": "markdown",
      "source": [
        "## How do the route numbers relate to the route type and load type?"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "a9876f0e-ee35-4617-a279-cf5661459188",
        "_uuid": "62381de3db1f9a1be9ebb620a9276c278be90ef4"
      },
      "source": [
        "routes = data.groupby('route_number')\n",
        "routes_by_route_type = routes['route_type'].nunique()\n",
        "routes_by_load_type = routes['load_type'].nunique()\n",
        "print('Redundant Route Types: {}'.format((routes_by_route_type > 1).sum()))\n",
        "print('Redundant Load Types: {}'.format((routes_by_load_type > 1).sum()))"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "831c0495-05ec-46af-a646-980560c73e51",
        "_uuid": "78eeefc703c47fc4e42ef51c97f3e75062f3f33b"
      },
      "cell_type": "markdown",
      "source": [
        "So this tells us the each route number is associated with only one route type but can be associated with more than one load type. It also means that the first few characters of a route number could potentially tell us what kind of route type it is. For example:"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "070019ac-8d81-4bb2-b5f8-da0c6254c732",
        "_uuid": "181b485f2f4db1eabf1529ad453e8bcaffa871fe"
      },
      "source": [
        "print('BULK: \\n{}\\n'.format(data[data['route_type'] == 'BULK']['route_number'].unique()))\n",
        "print('DEAD ANIMAL: \\n{}\\n'.format(data[data['route_type'] == 'DEAD ANIMAL']['route_number'].unique()))"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "1b899ef8-888e-4950-9ac7-44e174b00cb9",
        "_uuid": "f654da0171d5516964072978a113849a32dd483b"
      },
      "cell_type": "markdown",
      "source": [
        "All bulk route numbers start with \"BU\" while all dead animal route numbers start with \"DA\". Nothing groundbreaking here, just a little more good-to-know information in case the dataset grows."
      ]
    },
    {
      "metadata": {
        "_cell_guid": "8f888bd4-68d4-499b-ad69-6d498d3f5ee1",
        "_uuid": "ec7f607c0f6543792842e227f45d96967f857736"
      },
      "cell_type": "markdown",
      "source": [
        "## Now let's start looking at the dataset as a time-series"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "1e527558-d938-45f5-83ca-2988ab50dc82",
        "_uuid": "888bfdbe6010630ee457a66b1e84141f10eb7c5b"
      },
      "source": [
        "data_ts = data.sort_values('load_time')\n",
        "data_ts.index = data_ts['load_time']\n",
        "data_ts.drop('load_time', axis=1, inplace=True)\n",
        "data_ts.head()"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "3e96ec3b-1ca5-4f27-9d53-06dd46136261",
        "_uuid": "defc2cf54d768b48e7524a5eae29d5f498b35449"
      },
      "source": [
        "load_types = data_ts['load_type'].unique()\n",
        "skip_plots = []\n",
        "fig = plt.figure(figsize=(12,12))\n",
        "for i, lt in enumerate(load_types):\n",
        "    #resample the data to get monthly totals\n",
        "    tmp = data_ts[data_ts['load_type'] == lt]['load_weight'].resample('M').sum()\n",
        "    ax = fig.add_subplot(6, 3, i+1)\n",
        "    plt.plot(tmp.index, tmp.values)\n",
        "    ax.set_title(lt)\n",
        "    ax.set_xlim(data_ts.index.min(), data_ts.index.max())\n",
        "fig.tight_layout()"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "0054c508-2eae-44d1-bd41-dd84d4c67af2",
        "collapsed": true,
        "_uuid": "0f6a7b9ed667b84c71993fa2943907eb098eef88"
      },
      "cell_type": "markdown",
      "source": [
        "### Inital observations that need investigation:\n",
        "* Plots for bagged litter, xmas trees, mulch, recycling plastic bags, and matress are useless\n",
        "* Single stream recycling started around 2009\n",
        "    * This is when comingle and paper recycling stopped\n",
        "    * There was a downturn in garbage collection once single stream recycling started and has held steady since\n",
        "* Upward trend in single stream recycling?\n",
        "* Downward trend in street sweeping, litter, and dead animals?\n",
        "* Seems to be some seasonality in yard trimmings\n",
        "    * maybe brush, street sweeping, and ~~tires~~ too?\n",
        "    * fft for peak frequencies\n"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "d0b1bd6c-9ddc-47cb-b450-b110de9d1fc0",
        "_uuid": "585916169a4a3bb06b8a986eb616509435a0aa2a"
      },
      "source": [
        "yt = data_ts[data_ts['load_type'] == 'YARD TRIMMING']\n",
        "yt = yt.resample('M').sum()\n",
        "yt['load_weight'].plot()"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "7cc28d24-e6b4-48b8-956b-e213d4cd5101",
        "_uuid": "905f096b2fda36754b860c3fa7c40c21f0857710"
      },
      "cell_type": "markdown",
      "source": [
        "### There is definitely some seasonality here, let's get the monthly averages to see what the yearly cycle looks like"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "6e91ea00-3e2d-431e-8f5f-ab915de732cb",
        "_uuid": "9efc32a257e4bf6a354cd2154011839ed39cb7f1"
      },
      "source": [
        "plt.plot(yt.groupby(yt.index.month).mean()['load_weight'])"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "cd7c29c6-5ed4-4ae2-8d03-da203c8e94b2",
        "_uuid": "f2f6421dff2bdfffa4239a0e91d1b24891206756"
      },
      "cell_type": "markdown",
      "source": [
        "### So this makes sense, lots of yard trimmings in the spring, slowly dwindling as the brutal Texas summer sets in, smaller peak in fall, dips again in winter.\n",
        "I think it's pretty telling of our weather that there are more yards being mowed in the dead of winter than the dead of summer"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "72fa4188-3dcd-4f60-9206-312443d96616",
        "_uuid": "46367f006b9c595620e4701b4d664b926d4edc36"
      },
      "source": [
        "da = data_ts[data_ts['load_type'] == 'DEAD ANIMAL']\n",
        "da.resample('M').sum()['load_weight'].plot()"
      ]
    },
    {
      "metadata": {
        "_cell_guid": "d7d348f6-2035-4327-a9c4-83aa5fa11863",
        "_uuid": "048f141115240d2950d8ec101f2b48d61feda0d6"
      },
      "cell_type": "markdown",
      "source": [
        "### There is alot of information to be gleaned from this plot:\n",
        "* peak in late 2016 when Austin no-kill animal shelters became overcrowded and stopped taking rescues\n",
        "    * Intense flooding in 2016"
      ]
    },
    {
      "execution_count": null,
      "outputs": [],
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "f70dffc4-1e11-4e2e-a4b7-be0e086a0080",
        "collapsed": true,
        "_uuid": "14d4cc53662721aba8a0f86ae7e0b4170827f26b"
      },
      "source": []
    }
  ],
  "metadata": {
    "language_info": {
      "mimetype": "text/x-python",
      "codemirror_mode": {
        "version": 3,
        "name": "ipython"
      },
      "pygments_lexer": "ipython3",
      "nbconvert_exporter": "python",
      "file_extension": ".py",
      "version": "3.6.1",
      "name": "python"
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3",
      "language": "python"
    }
  }
}