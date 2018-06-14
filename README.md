# News Sentiment Analysis 

By *Aidin Hassanzadeh*
___

This repository contains Python/NootebookIPython files for the 'News Sentiment Analysis' project.
The aim of this project is to perform quantitative analysis of different weather trend data with respect to latitude.

## Data
The data utilized in this analysis work is obtained by Twitter API on 06.14.2018 17:10 (UTC). The sentiments of tweets are estimated by [VADER-Sentiment-Analysis](https://github.com/cjhutto/vaderSentiment). 

## Report
The visual report containing the discovered insights and the detailed implementation are available by a Jupyter Noebook [here](https://github.com/aidinhass/newssentiment/blob/master/notebooks/README.md).

## Requirements
- python=3.6.5
- jupyter=1.0.0
- nb_conda=2.2.1
- numpy=1.14.2
- matplotlib=2.2.2
- pandas=0.22.0
- scipy=1.1.0
- vaderSentiment

## Directory Structure

```bash
.
├── docs                <- Documents related to this project.    
├── images              <- Images for README.md files.
├── newssentiment       <- source files used in this project.
│   ├── conf
│   ├── data
│   │   ├── ext
│   │   ├── int
│   │   └── raw
│   ├── images
│   ├── plot
│   └── scripts
├── notebooks           <- Ipythoon Notebook files
├── reports             <- Generated analysis as HTML, PDF, Latex, etc.
│   ├── figures         <- Generated graphics and figures used in reporting.
│   └── logs            <- Generated log files.
└── scripts             <- Scripts used in this project.

```

### Installation
Install python dependencies from  `requirements.txt` using conda.
```bash
conda install --yes --file requirements.txt
```

Or create a new conda environment `<new-env-name>` by importing a copy of a working conda environment stored at root directory :`weatherpy.yml`.
```bash
conda env create --name <new-env-name> -f "newssentimentpy.yml"
```

## References
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

## To Do
- [ ] Test News Sentiment tweeter bot 

## License
NA
