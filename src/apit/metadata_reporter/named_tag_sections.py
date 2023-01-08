from apit.readable_names import ReadableTagName

ORDER_TRACK = [
    ReadableTagName.TITLE,
    ReadableTagName.SORT_ORDER_TITLE,
    ReadableTagName.ARTIST,
    ReadableTagName.SORT_ORDER_ARTIST,
    ReadableTagName.COMPOSER,
    ReadableTagName.SORT_ORDER_COMPOSER,
    ReadableTagName.TRACK_NUMBER,
    ReadableTagName.RATING,
    ReadableTagName.GAPLESS,
    ReadableTagName.BPM,
    ReadableTagName.MEDIA_TYPE,
]
ORDER_ALBUM = [
    ReadableTagName.ALBUM_NAME,
    ReadableTagName.SORT_ORDER_ALBUM,
    ReadableTagName.ALBUM_ARTIST,
    ReadableTagName.SORT_ORDER_ALBUM_ARTIST,
    ReadableTagName.DISC_NUMBER,
    ReadableTagName.COMPILATION,
    ReadableTagName.GENRE,
    ReadableTagName.RELEASE_DATE,
    ReadableTagName.COPYRIGHT,
]
ORDER_IDS = [
    ReadableTagName.CONTENT_ID,
    ReadableTagName.PLAYLIST_ID,
    ReadableTagName.ARTIST_ID,
    ReadableTagName.GENRE_ID,
    ReadableTagName.COMPOSER_ID,
    ReadableTagName.ISRC_ID,
]
ORDER_MISC = [
    ReadableTagName.TOOL,
    ReadableTagName.GROUPING,
    ReadableTagName.COMMENT,
    ReadableTagName.ARTWORK,
    ReadableTagName.LYRICS,
]
ORDER_USER = [
    ReadableTagName.OWNER_NAME,
    ReadableTagName.USER_MAIL,
    ReadableTagName.PURCHASE_DATE,
    ReadableTagName.STOREFRONT_ID,
]
