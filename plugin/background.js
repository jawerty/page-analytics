const experimentA = () => {
  // nightmare before christmas experiment
  const searchQueries = [
    "jack skellington",
    "nightmare before christmas",
    "sally and jack",
    "tim burton",
    "nightmare before xmas",
    "oogy boogy",
    "oogie boogie",
    "jack nightmare before christmas",
    "this is halloween",
    "making christmas",
    "jack and sally montage",
    "jack's obsession",
    "santa from nightmare before christmas",
    "danny elfman soundtrack",
    "best jack skellington scenes",
    "pumpkin king",
    "jack skellington broadway",
    "jack skellington real life",
    "tim burton nightmare christmas",
    "oogie boogie jack skellington",
    "nightmare before christmas sally",
    "nightmare before christmas jack",
    "animation stop motion tim burton",
  ];

  const getRandomSearchQuery = () => {
    return searchQueries[Math.floor(Math.random() * searchQueries.length)];
  };

  const youtubeSearch = () => {
    return new Promise((resolve, reject) => {
      const searchQuery = getRandomSearchQuery();
      console.log(searchQuery);
      const url = `https://www.youtube.com/results?search_query=${encodeURIComponent(
        searchQuery
      )}`;
      const headers = new Headers({
        "User-Agent":
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
      });

      fetch(url, {
        method: "GET",
        headers,
      })
        .then(() => {
          resolve(searchQuery);
        })
        .catch((e) => {
          reject(e);
        });
    });
  };

  const postSearchQuery = async (searchQueryToSave) => {
    const data = {
      query: searchQueryToSave,
      experimentType: "experimentA",
      resultKeywords: [],
    };

    try {
      const response = await fetch("http://localhost:5000/q", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      return response;
    } catch (e) {
      console.log(e);
    }
  };

  setInterval(async () => {
    const searchQueryToSave = await youtubeSearch();
    const postResponse = await postSearchQuery(searchQueryToSave);
    console.log(postResponse);
  }, 1000 * 60);
};

(function main() {
  experimentA();
  // run experiments
})();
