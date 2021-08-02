
INSERT INTO searchQuery(
 -- 0
    query,
    experimentType,
    resultKeywords
)

VALUES {}
;

INSERT INTO video (
-- 1
    videoURL,
    videoID,
    keywords,
    experimentSource,
    recommededVideo,
    parentRecommended,
    videoViews,

)

VALUES {}
;

INSERT INTO keywords (
-- 2
    word,
    cnt,
    pos, 
    sentiment
)
VALUES {}
;

-- 3
SELECT word FROM keywords WHERE word = {}
;
-- 4
UPDATE keywords SET cnt = {} WHERE word = {}
;