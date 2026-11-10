.class public final Lcom/privacyfblite/extension/Block;
.super Ljava/lang/Object;

.method private constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public static shouldBlock(Ljava/lang/String;)Z
    .locals 3
    if-nez p0, :no
    invoke-virtual {p0}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;
    move-result-object v0

    # telemetry / analytics
    invoke-static {}, Lcom/privacyfblite/extension/Config;->blockTelemetry()Z
    move-result v1
    if-eqz v1, :chk_ads
    const-string v1, "telemetry"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "analytics"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "/tr/"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "/ajax/bz"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "pixel.facebook"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "snaptu-z.facebook"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "logging_client"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "perflogger"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "profilo"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "graph.facebook.com/logging"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes

    :chk_ads
    invoke-static {}, Lcom/privacyfblite/extension/Config;->blockAds()Z
    move-result v1
    if-eqz v1, :chk_feed
    const-string v1, "/ads/"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "ads.facebook"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "an.facebook.com"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "sponsored"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes

    :chk_feed
    invoke-static {}, Lcom/privacyfblite/extension/Config;->blockFeed()Z
    move-result v1
    if-eqz v1, :chk_reels
    const-string v1, "newsfeed"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "news_feed"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "feed_unit"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "/feed/"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes

    :chk_reels
    invoke-static {}, Lcom/privacyfblite/extension/Config;->blockReels()Z
    move-result v1
    if-eqz v1, :chk_pymk
    const-string v1, "reels"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "short_form"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "heroplayer"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "mediastreaming"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "fb_shorts"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes

    :chk_pymk
    invoke-static {}, Lcom/privacyfblite/extension/Config;->blockPymk()Z
    move-result v1
    if-eqz v1, :no
    const-string v1, "pymk"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "people_you_may_know"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    goto :no

    :yes
    const/4 v0, 0x1
    return v0
    :no
    const/4 v0, 0x0
    return v0
.end method
