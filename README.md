# Waterfall Engine

<hr/>

### Some important information:
- GitHub link for code repository: https://github.com/i5m/waterfall
- It’s very simple and intuitive to run on a machine. The steps are mentioned in this file.
- This file also contains the process I went through and some future works I'd be interested in learning and implementing.

<hr/>

### There are two ways to tackle this challenge:

- Where we can use the pandas module in python to make it easier to process data and produce results. In this approach, upon asking for waterfall for each investor, we can do it by:
    - Using methods of the pandas library to filter out the required rows and clean column values.
    - Create desired data structure to organize information needed for calculations.
    - ​​Run our logic on the extracted and organized data.

- Where we load data into custom classes models. This approach helps us ensure data integrity and allows us to write more robust code for further development. We will use the following strategy:
    - Go over the data and create model objects for each important information
    - While creating models, also create required data structure and store them to produce faster runtime results if in case using database
    - Process the waterfall logic on the models and produce relevant output

Based on my discussion with AJ, the waterfall will be processed for the final distribution. Alright, let’s get started with the 2nd approach.

<hr/>

### Running the application

Please make sure that you have necessary modules installed by running:

```py
pip3 install pandas tabulate
```

Now, you can run the program by simply:

```py
python3 main.py
```

The program will ask you for an ID. After providing the ID, it'll start processing the data and outputs the results and other essential information.

<hr/>

### Tests

You can run the application on a sample dataset as well which was built using the example given in the assesment PDF by adding the --example flag in the command:

```py
python3 main.py --example
```

It'll ask you for the ID and you can enter 1 to compare the table produced by the program with what is available in the PDF.

#### Also
There are various tests written for each of the functions that has been used throughout the lifecycle of the program. I have written few unit tests for each of them which can be tested using the following command:

```py
python3 unit_tests.py
```

<hr/>

### Future Works

#### Waterfall for various distributions

My biggest concern while discussing with AJ about the engine was on handling multiple distribution. The code handles the last distribution based on our disucssion. But it'd be super interesting to see how in real-life the flow works to handle multiple distribution wherein the capital keeps on changing and therfore all other tiers as well.

#### Working with multiple vendors and funds

The application right now supports data for one enterprise only. It'll be interesting to build an infrasturture and pipeline to support various enterprises with unique needs for loading, processing, results.

#### Adding UI for ease of use

Building a good user-experience is equally important to deliver a solid product. I wish to build a user interface where users can upload the data and start interacting with it in some meaningful ways such as running waterfall on specific distributions or with different config options.

