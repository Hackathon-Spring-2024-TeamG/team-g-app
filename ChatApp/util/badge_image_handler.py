from util.enums import BadgeType

def determineImageUrl(badge_type):
    badge_image_urls = {
        BadgeType.FAST_PARROT: "/static/img/fast_parrot.gif",
        BadgeType.ANGEL_PARROT: "/static/img/angel_parrot.gif",
    }
    return badge_image_urls.get(badge_type, "/static/img/fast_parrot.gif")