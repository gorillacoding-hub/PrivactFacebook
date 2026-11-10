.class public final Lcom/privacyfblite/extension/Config;
.super Ljava/lang/Object;

# static fields
.field private static prefs:Landroid/content/SharedPreferences;

# direct methods
.method static constructor <clinit>()V
    .locals 0
    return-void
.end method

.method private constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public static init(Landroid/content/Context;)V
    .locals 3
    if-nez p0, :done
    sget-object v0, Lcom/privacyfblite/extension/Config;->prefs:Landroid/content/SharedPreferences;
    if-eqz v0, :done
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;
    move-result-object v0
    const-string v1, "privacyfblite_prefs"
    const/4 v2, 0x0
    invoke-virtual {v0, v1, v2}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v0
    sput-object v0, Lcom/privacyfblite/extension/Config;->prefs:Landroid/content/SharedPreferences;
    :done
    return-void
.end method

.method public static get(Ljava/lang/String;Z)Z
    .locals 2
    sget-object v0, Lcom/privacyfblite/extension/Config;->prefs:Landroid/content/SharedPreferences;
    if-nez v0, :def
    invoke-interface {v0, p0, p1}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z
    move-result v0
    return v0
    :def
    return p1
.end method

.method public static set(Ljava/lang/String;Z)V
    .locals 2
    sget-object v0, Lcom/privacyfblite/extension/Config;->prefs:Landroid/content/SharedPreferences;
    if-nez v0, :done
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    invoke-interface {v0, p0, p1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->commit()Z
    :done
    return-void
.end method

.method public static blockTelemetry()Z
    .locals 2
    const-string v0, "block_telemetry"
    const/4 v1, 0x1
    invoke-static {v0, v1}, Lcom/privacyfblite/extension/Config;->get(Ljava/lang/String;Z)Z
    move-result v0
    return v0
.end method

.method public static blockAds()Z
    .locals 2
    const-string v0, "block_ads"
    const/4 v1, 0x1
    invoke-static {v0, v1}, Lcom/privacyfblite/extension/Config;->get(Ljava/lang/String;Z)Z
    move-result v0
    return v0
.end method

.method public static blockFeed()Z
    .locals 2
    const-string v0, "block_feed"
    const/4 v1, 0x1
    invoke-static {v0, v1}, Lcom/privacyfblite/extension/Config;->get(Ljava/lang/String;Z)Z
    move-result v0
    return v0
.end method

.method public static blockReels()Z
    .locals 2
    const-string v0, "block_reels"
    const/4 v1, 0x1
    invoke-static {v0, v1}, Lcom/privacyfblite/extension/Config;->get(Ljava/lang/String;Z)Z
    move-result v0
    return v0
.end method

.method public static blockPymk()Z
    .locals 2
    const-string v0, "block_pymk"
    const/4 v1, 0x1
    invoke-static {v0, v1}, Lcom/privacyfblite/extension/Config;->get(Ljava/lang/String;Z)Z
    move-result v0
    return v0
.end method
