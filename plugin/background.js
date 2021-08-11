const postSearchQuery = async (experimentName, searchQueryToSave) => {
  const data = {
    query: searchQueryToSave,
    experimentType: `experiment${experimentName}`,
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

// get recommended videos
const postVideo = async (experimentName, videoToSave) => {
  const data = {
    ...videoToSave,
    experimentSource: experimentName,
  };

  try {
    const response = await fetch("http://localhost:5000/video", {
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

const youtubeExperiment = (experimentName, searchQueries) => {
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

  const searchRoutine = async () => {
    const searchQueryToSave = await youtubeSearch();
    console.log(`Running new search with query "${searchQueryToSave}"`);
    const postResponse = await postSearchQuery(
      experimentName,
      searchQueryToSave
    );
    console.log("end search", postResponse);
  };

  searchRoutine();
  setInterval(searchRoutine, 1000 * 60 * 10);

  const processMessage = (request) => {
    return new Promise(async (resolve, reject) => {
      if (request.eventName === "recommendedContent") {
        console.log("Got recommended content");
        const recommendedVideo = request.data.content;
        const response = await postVideo(experimentName, recommendedVideo);
        console.log(response);
        resolve(true);
      }
    });
  };
  chrome.runtime.onMessage.addListener(function (
    request,
    sender,
    sendResponse
  ) {
    processMessage(request).then((response) => {
      sendResponse(response);
    });
    return true;
  });
};

const runExperiment = (options) => {
  if (options.type === "youtube") {
    youtubeExperiment(options.name, options.topics);
  }
};

(function main() {
  // run experiments
  runExperiment({
    name: "A",
    type: "youtube",
    topics: [
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
    ],
  });
})();
