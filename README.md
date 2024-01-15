# FLowSH

FLowSH is a resilient system that discovers web attack on the network traffic based on similarity search techniques. Here is a content guide.
## Content
This project has four main folders. 
1. The **FLowSH** folder with the current implementation of the system.
2. The **LSH Evaluation** folder with all the evaluation performed on the Similarity Search Engine.
3. The **Netflow Evaluation** folder with all the files used for the netflow evaluation.


## System Guide
The system is composed by 4 modules: **WebFlow**, **Log Extractor**, **Similarity Search Engine** and **String Analyser**. The system workflow is followed in the same order.

### WebFlow
This module has 3 main blocks. 
1. The Exporter that exports the network traffic into a pcap format.
2. The Collector that collects this pcap format network traffic into a CSV format to be analysed. Can be ran using a shell script file.
3. The Analyser that detect the anomalous network traffic using the unsupervised machine learning models. The respective folder has the main models used.

### Log Extractor
This module has 2 blocks.
1. The Filter block which gets the log chunks corresponding to the datetime requested.
2. The Parser block that parses the chunk logs to have a steady stream of logs.

Both blocks are implemented in python 3.8V.

### Similarity Search Engine
This module has 3 main blocks.
1. Token Builder, that creates the MinHash to be queried in the LSH.
2. Token Query, that queries the MinHash object in the LSH.
3. Token Classifier, receives the keys returned in the Token Query and decides if the token is a web attack or not.
4. LSH Updater, updates the LSH with the given MinHash.

All the blocks are implemented in python 3.8V.

### String Analyser
This module is activated if the Similarity Search Engine is not conclusive. It is implemented in python 3.8V.

## How to use
Every module has a function defined with the same name, they are highly modular, meaning they can be called anytime without  any big dependencies.