
    var chart_config = {
        chart: {
            container: "#collapsable-example",

            animateOnInit: true,
            
            node: {
                collapsable: true
            },
            animation: {
                nodeAnimation: "easeOutBounce",
                nodeSpeed: 700,
                connectorsAnimation: "bounce",
                connectorsSpeed: 700
            }
        },
        nodeStructure: {
            image: "bbbbb",
            children: [
                {
                    image: "/static/treant-js-master/collapsable/img/lana.png",
                    collapsed: true,
                    children: [
                        {
                            image: "/static/treant-js-master/collapsable/img/figgs.png"
                        }
                    ]
                },
                {
                    image: "/static/treant-js-master/collapsable/img/sterling.png",
                    childrenDropLevel: 1,
                    children: [
                        {
                            image: "/static/treant-js-master/collapsable/img/woodhouse.png"
                        }
                    ]
                },
                {
                    pseudo: true,
                    children: [
                        {
                            image: "/static/treant-js-master/collapsable/img/cheryl.png"
                        },
                        {
                            image: "/static/treant-js-master/collapsable/img/pam.png"
                        }
                    ]
                }
            ]
        }
    };

 /*Array approach
    var config = {
        container: "#collapsable-example",

        animateOnInit: true,
        
        node: {
            collapsable: true
        },
        animation: {
            nodeAnimation: "easeOutBounce",
            nodeSpeed: 700,
            connectorsAnimation: "bounce",
            connectorsSpeed: 700
        }
    },
    malory = {
        image: "/static/treant-js-master/collapsable/img/malory.png"
    },

    lana = {
        parent: malory,
        image: "/static/treant-js-master/collapsable/img/lana.png"
    }

    figgs = {
        parent: lana,
        image: "/static/treant-js-master/collapsable/img/figgs.png"
    }

    sterling = {
        parent: malory,
        childrenDropLevel: 1,
        image: "/static/treant-js-master/collapsable/img/sterling.png"
    },

    woodhouse = {
        parent: sterling,
        image: "/static/treant-js-master/collapsable/img/woodhouse.png"
    },

    pseudo = {
        parent: malory,
        pseudo: true
    },

    cheryl = {
        parent: pseudo,
        image: "/static/treant-js-master/collapsable/img/cheryl.png"
    },

    pam = {
        parent: pseudo,
        image: "/static/treant-js-master/collapsable/img/pam.png"
    },

    chart_config = [config, malory, lana, figgs, sterling, woodhouse, pseudo, pam, cheryl];*/

