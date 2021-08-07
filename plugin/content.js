const experimentA = () => {
  window.addEventListener(
    "DOMContentLoaded",
    function (event) {
      if (window.location.hostname === "www.youtube.com") {
        console.log("Running page analytics");
        function isHomepage() {
          const home = document.querySelector('[page-subtype="home"]');
          return home && home.getAttribute("role") == "main";
        }

        function homepageContentLoaded() {
          const content = document.querySelector("#overlays.ytd-thumbnail");
          return !!content;
        }

        function sendRecommendedVideos(recommendedVideos) {
          chrome.runtime.sendMessage(
            {
              eventName: "recommendedContent",
              data: {
                origin: "youtube",
                content: recommendedVideos,
              },
            },
            (response) => {
              console.log(response);
            }
          );
        }

        function waitForHomepage() {
          return new Promise(function (resolve, reject) {
            const interval = 100;
            let timeout = 0;
            const homepageWait = setInterval(function () {
              timeout += interval;
              console.log(isHomepage() == true);
              if (isHomepage() == true && homepageContentLoaded() == true) {
                clearInterval(homepageWait);
                resolve(true);
              } else if (timeout > 5000) {
                // stop after a while
                reject();
              }
            }, interval);
          });
        }

        function getVideoPageInfo(videoUrl) {
          return new Promise(async (resolve, reject) => {
            const headers = new Headers({
              "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            });

            fetch(videoUrl, {
              method: "GET",
              credentials: "omit",
              headers,
            })
              .then(function (response) {
                return response.text();
              })
              .then(function (text) {
                const doc = document.implementation.createHTMLDocument("");
                doc.open();
                doc.write(text);
                doc.close();
                console.log(doc);

                const scripts = doc.evaluate(
                  '//script[contains(text(),"ytInitialData")]',
                  doc.body,
                  null,
                  XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
                  null
                );
                const results = [];
                for (
                  let i = 0, length = scripts.snapshotLength;
                  i < length;
                  ++i
                ) {
                  results.push(scripts.snapshotItem(i));
                }
                const unparsedJSON = results[0].innerText
                  .split("var ytInitialData = ")[1]
                  .trim();

                console.log(unparsedJSON);
                const ytData = JSON.parse(
                  unparsedJSON.substring(0, unparsedJSON.length - 1)
                );

                let views;
                try {
                  views =
                    ytData.playerOverlays.playerOverlayRenderer.videoDetails
                      .playerOverlayVideoDetailsRenderer.subtitle.runs[2].text;
                } catch (e) {
                  console.log(e);
                }

                const keywordsMetaTag = doc.head.querySelector(
                  'meta[name="keywords"]'
                );
                console.log(doc.head, keywordsMetaTag);
                const keywords = keywordsMetaTag
                  .getAttribute("content")
                  .split(", ");

                const videoViews = parseInt(
                  views.split(" views")[0].replaceAll(",", "")
                );
                resolve({ keywords, videoViews });
              })
              .catch(function (err) {
                console.log(err);
                reject(err);
              });
          });
        }

        (async function main(pageToWaitFor) {
          if (pageToWaitFor == "home") {
            await waitForHomepage(); // wait for content to render
          }
          if (isHomepage()) {
            function getRecommendedVideos() {
              return new Promise(async (resolve) => {
                let recommendedVideosByDetails = document.querySelectorAll(
                  "#content ytd-rich-item-renderer #details"
                );
                const recommendedVideos = [];
                for (const recommendedVideo of recommendedVideosByDetails) {
                  const creatorName =
                    recommendedVideo.querySelector("#avatar-link").title;
                  const titleLinkEl =
                    recommendedVideo.querySelector("#video-title-link");
                  const titleLink = titleLinkEl.href;
                  const videoID = titleLink.split("?v=")[1];
                  const videoURL = titleLink;

                  let results = {};
                  try {
                    results = await getVideoPageInfo(videoURL);
                  } catch (e) {
                    console.log(e);
                  }
                  const recommendedVideoObject = {
                    creatorName,
                    title: titleLinkEl.innerText,
                    videoURL,
                    videoID,
                    recommededVideo: true,
                    ...results,
                  };

                  recommendedVideos.push(recommendedVideoObject);
                }

                resolve(recommendedVideos);
              });
            }

            const recommendedVideos = await getRecommendedVideos();
            console.log(recommendedVideos);
            sendRecommendedVideos(recommendedVideos);
          }
        })();
      }
    },
    { passive: true }
  );
};

(function main() {
  experimentA();
})();
