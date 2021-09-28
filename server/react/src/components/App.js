import { useEffect, useState } from "react"
import ExperimentCard from "./ExperimentCard"

function App() {
    const [experiments, setExperiments] = useState([])

    const getExperiments = () => {
        return fetch("/experiments", "GET")
    }

    useEffect(() => {
        if (experiments.length === 0) {
            getExperiments().then((experimentData) => {
                setExperiments(experimentData)
            })
        }
    })

    return (
        <div className="app">
            Amount of experiments we have {experiments.length}
            {experiments && experiments.map((experimentData) => {
                return <ExperimentCard experiment={experimentData} />
            })}

        </div>
    )
}

export default App