
INSERT INTO searchQuery(
 -- 0
    query,
    experimentType,
    resultKeywords
)

VALUES (%s, %s, %s)
;

INSERT INTO video (
-- 1
    videoURL,
    videoID,
    keywords,
    experimentSource,
    videoViews

)

VALUES (%s, %s, %s, %s, %s)
;

INSERT INTO keyword (
-- 2
    word,
    cnt
)
VALUES (%s, %s)
;

-- 3
SELECT word FROM keyword WHERE word = '%s'
;
-- 4
UPDATE keyword SET cnt = %s WHERE word = '%s'
;