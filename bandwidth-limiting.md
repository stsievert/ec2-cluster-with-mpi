
A couple steps are required to tune the bandwidth:

1. Install dependencies
2. Test the bandwidth between two machines
3. Change the bandwith

Changing the bandwidth does require some fraction of the default bandwidth for
g2.2s. VGG-19 has 134M params () and ResNet-32 has 0.46M parameters (). This suggests
we should set the bandwidth to be $0.46 / 134 = 0.00343$. I encourage testing
this.

## Choosing percentage
Number of parameters:

* VGG-19: ~135 million (table 2 of simonyan2014very)
* Xception: ~22 million (table 3 chollet2016xception)
* Inception V3: 23 million (table 3 chollet2016xception)
* ResNet 32: 0.46 million (table 6 of he2016)
* ResNet 110: 1.7 million (table 6 of he2016)
* ResNet 1202: 19.4 million (table 6 of he2016)

The cite keys are below in references.

## Setup
Copy and paste this into your shell:

``` shell
function install {
    sudo yum install -y trickle
    sudo yum install -y iperf
}

function limit_band() {
    # first argument: fraction of g2.2 bandwidth desired
    default=$(echo "1024 * 1024 / 8;" | bc)
    band=$(echo "$1 * $default;" | bc)
    echo "---------------------------------------------------------------------"
    echo "Entering new shell that is band limited. Use "exit" or <Cntrl>D to
    echo "exit this shell and remove the bandwidth limits"
    echo ""
    echo "(upload and download bandwidth limited to $1 of the g2.2 default
    bandwidth)"
    echo "---------------------------------------------------------------------"
    trickle -s -u $band -d $band bash
}
function test_server() {
    iperf -s -p 3141
}

function test_client() {
    # first argument: Server address, or AWS IPv4 public IP
    iperf -c $1 -p 3141
}
```

## Install
```
install
```

## Limit bandwidth
``` shell
limit_band 0.5
```

This will launch a new shell in which all new threads/processes will have
limited bandwidth of 0.5 the default for g2.2 machines (1Gbit/s; tested).

This will require pasting the functions above into your shell again.

## Test
``` shell
# sever machien
test_server

# client machine
test_client {IPv4 public IP address}
```

## References
* simonyan2014very

    @Article{simonyan2014very,
    author = {Simonyan, Karen and Zisserman, Andrew},
    title = {Very deep convolutional networks for large-scale image recognition},
    journal = {arXiv preprint arXiv:1409.1556},
    volume = {},
    number = {},
    pages = {},
    year = {2014},
    abstract = {},
    location = {},
    keywords = {imagenet}}

* chollet2016xception

    @Proceedings{he2016,
    author = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
    editor = {},
    title = {Deep residual learning for image recognition},
    booktitle = {Deep residual learning for image recognition},
    volume = {Proceedings of the IEEE conference on computer vision and pattern recognition},
    publisher = {},
    address = {},
    pages = {770-778},
    year = {2016},


* he2016

    @Proceedings{he2016,
    author = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
    editor = {},
    title = {Deep residual learning for image recognition},
    booktitle = {Deep residual learning for image recognition},
    volume = {Proceedings of the IEEE conference on computer vision and pattern recognition},
    publisher = {},
    address = {},
    pages = {770-778},
    year = {2016}}

