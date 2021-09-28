function _g_r_c_() {
    let result = {
        ads: [],
        videos: []
    };
    try {
        const twoColumnRenderer = window.ytcfg.data_.SBOX_SETTINGS.SEARCHBOX_COMPONENT.__dataHost.parentComponent.__data.data.response.contents.twoColumnBrowseResultsRenderer;
        if (twoColumnRenderer.tabs.length > 0) {
            const videoContentArray = twoColumnRenderer.tabs[0].tabRenderer.content.richGridRenderer.contents;
            if (videoContentArray) {
                for (var i = 0; i < videoContentArray.length; i++) {
                    videoContent = videoContentArray[i];

                    if (videoContent.richItemRenderer) {
                        console.log(videoContent.richItemRenderer.content);
                        const adMetadata = {};
                        const videoMetadata = {};
                        const videoRenderer = videoContent.richItemRenderer.content.videoRenderer;
                        const displayAdRenderer = videoContent.richItemRenderer.content.displayAdRenderer;
                        if (displayAdRenderer) {
                            if (displayAdRenderer.bodyText) {
                                adMetadata.adDescription = displayAdRenderer.bodyText.simpleText;
                            }
                            if (displayAdRenderer.clickCommand && displayAdRenderer.clickCommand.urlEndpoint) {
                                adMetadata.url = displayAdRenderer.clickCommand.urlEndpoint.url;
                            }
                            if (displayAdRenderer.secondaryText) {
                                adMetadata.adProvider = displayAdRenderer.secondaryText.simpleText;
                            }
                            if (displayAdRenderer.titleText) {
                                adMetadata.adTitle = displayAdRenderer.titleText.simpleText;
                            }
                            result['ads'].push(adMetadata)
                        }
                        if (videoRenderer) {
                            if (videoRenderer.videoId) {
                                videoMetadata.videoId = videoRenderer.videoId
                            }
                            if (videoRenderer.ownerText && videoRenderer.ownerText.runs && videoRenderer.ownerText.runs.length > 0) {
                                videoMetadata.videoCreator = videoRenderer.ownerText.runs[0].text
                            }
                            if (videoRenderer.lengthText && videoRenderer.lengthText.simpleText) {
                                videoMetadata.videoLength = videoRenderer.lengthText.simpleText
                            }
                            if (videoRenderer.descriptionSnippet && videoRenderer.descriptionSnippet.runs && videoRenderer.descriptionSnippet.runs.length > 0) {
                                videoMetadata.videoDescription = videoRenderer.descriptionSnippet.runs[0].text
                            }
                            if (videoRenderer.publishedTimeText && videoRenderer.publishedTimeText.simpleText) {
                                videoMetadata.relativePublishTime = videoRenderer.publishedTimeText.simpleText;
                            }
                            if (videoRenderer.viewCountText && videoRenderer.viewCountText.simpleText) {
                                videoMetadata.videoViewsText = videoRenderer.viewCountText.simpleText;
                            }
                            result["videos"].push(videoMetadata)
                        }
                    }
                }
            }
        }
    } catch (e) {
        console.log(e);
        result = null;
    }
    return result;
};
return _g_r_c_();