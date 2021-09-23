function ExperimentCard({ experiment }) {
    return (
        <div className="experiment-card">
            <img src={experiment.imageSource}></img>
            <h2>{experiment.name}</h2>
            <p>{experiment.description}</p>
        </div>
    )
}

export default ExperimentCard;