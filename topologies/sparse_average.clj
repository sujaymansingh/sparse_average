(ns sparse_average
  (:use     [streamparse.specs])
  (:gen-class))


(defn sparse_average [options]
    [
        {
            "getdocuments-spout" (python-spout-spec
                options
                "getdocuments.GetDocumentsSpout"
                ["document"]
                )
        }

        {
            "summarise-bolt" (python-bolt-spec
                options
                {"getdocuments-spout" :shuffle}
                "summarise.SummariseBolt"
                ["document_with_summary"]
                :p 1
            )

            "calcaverage-bolt" (python-bolt-spec
                options
                {"summarise-bolt" :shuffle}
                "calcaverage.CalcAverageBolt"
                ["document_with_average"]
                :p 1
            )

            "index-bolt" (python-bolt-spec
                options
                {"calcaverage-bolt" :shuffle}
                "index.IndexBolt"
                ["document"]
                :p 1
            )
        }
    ]
)
