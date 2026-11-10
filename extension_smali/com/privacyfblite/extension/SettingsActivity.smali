.class public Lcom/privacyfblite/extension/SettingsActivity;
.super Landroid/app/Activity;

# instance fields
.field private scroll:Landroid/widget/ScrollView;
.field private layout:Landroid/widget/LinearLayout;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .locals 8
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    invoke-static {p0}, Lcom/privacyfblite/extension/Config;->init(Landroid/content/Context;)V

    new-instance v0, Landroid/widget/ScrollView;
    invoke-direct {v0, p0}, Landroid/widget/ScrollView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, Lcom/privacyfblite/extension/SettingsActivity;->scroll:Landroid/widget/ScrollView;

    new-instance v1, Landroid/widget/LinearLayout;
    invoke-direct {v1, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V
    iput-object v1, p0, Lcom/privacyfblite/extension/SettingsActivity;->layout:Landroid/widget/LinearLayout;
    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->setOrientation(I)V
    const/16 v2, 0x30
    const/16 v3, 0x30
    const/16 v4, 0x30
    const/16 v5, 0x30
    invoke-virtual {v1, v2, v3, v4, v5}, Landroid/widget/LinearLayout;->setPadding(IIII)V
    const/high16 v2, -0x1000000
    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    # Title
    new-instance v2, Landroid/widget/TextView;
    invoke-direct {v2, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V
    const-string v3, "PrivacyFBLite Settings"
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
    const/high16 v3, 0x41c00000    # 24.0f
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextSize(F)V
    const/4 v3, -0x1
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextColor(I)V
    const/16 v3, 0x0
    const/16 v4, 0x0
    const/16 v5, 0x0
    const/16 v6, 0x20
    invoke-virtual {v2, v3, v4, v5, v6}, Landroid/widget/TextView;->setPadding(IIII)V
    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    # Subtitle
    new-instance v2, Landroid/widget/TextView;
    invoke-direct {v2, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V
    const-string v3, "Toggle blocks. Tap Apply & Restart to take effect."
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
    const/high16 v3, 0x41600000    # 14.0f
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextSize(F)V
    const v3, -0x333334
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextColor(I)V
    const/16 v3, 0x0
    const/16 v4, 0x0
    const/16 v5, 0x0
    const/16 v6, 0x18
    invoke-virtual {v2, v3, v4, v5, v6}, Landroid/widget/TextView;->setPadding(IIII)V
    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    # Checkboxes
    const-string v2, "block_telemetry"
    const-string v3, "Block telemetry / analytics"
    const/4 v4, 0x1
    invoke-direct {p0, v1, v2, v3, v4}, Lcom/privacyfblite/extension/SettingsActivity;->addToggle(Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;Z)V

    const-string v2, "block_ads"
    const-string v3, "Block ads"
    const/4 v4, 0x1
    invoke-direct {p0, v1, v2, v3, v4}, Lcom/privacyfblite/extension/SettingsActivity;->addToggle(Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;Z)V

    const-string v2, "block_feed"
    const-string v3, "Block News Feed ranking paths"
    const/4 v4, 0x1
    invoke-direct {p0, v1, v2, v3, v4}, Lcom/privacyfblite/extension/SettingsActivity;->addToggle(Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;Z)V

    const-string v2, "block_reels"
    const-string v3, "Block Reels / short video paths"
    const/4 v4, 0x1
    invoke-direct {p0, v1, v2, v3, v4}, Lcom/privacyfblite/extension/SettingsActivity;->addToggle(Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;Z)V

    const-string v2, "block_pymk"
    const-string v3, "Block PYMK / suggestions"
    const/4 v4, 0x1
    invoke-direct {p0, v1, v2, v3, v4}, Lcom/privacyfblite/extension/SettingsActivity;->addToggle(Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;Z)V

    # Apply button
    new-instance v2, Landroid/widget/Button;
    invoke-direct {v2, p0}, Landroid/widget/Button;-><init>(Landroid/content/Context;)V
    const-string v3, "Apply & Restart App"
    invoke-virtual {v2, v3}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V
    const/16 v3, 0x0
    const/16 v4, 0x20
    const/16 v5, 0x0
    const/16 v6, 0x0
    invoke-virtual {v2, v3, v4, v5, v6}, Landroid/widget/Button;->setPadding(IIII)V
    new-instance v3, Lcom/privacyfblite/extension/SettingsActivity$1;
    invoke-direct {v3, p0}, Lcom/privacyfblite/extension/SettingsActivity$1;-><init>(Lcom/privacyfblite/extension/SettingsActivity;)V
    invoke-virtual {v2, v3}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    # Note
    new-instance v2, Landroid/widget/TextView;
    invoke-direct {v2, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V
    const-string v3, "\nOpen this screen anytime from the second launcher icon: PrivacyFBLite Settings.\nMessaging stays available. Server-driven Bloks UI may still show empty placeholders."
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
    const/high16 v3, 0x41400000    # 12.0f
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextSize(F)V
    const v3, -0x666667
    invoke-virtual {v2, v3}, Landroid/widget/TextView;->setTextColor(I)V
    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    invoke-virtual {v0, v1}, Landroid/widget/ScrollView;->addView(Landroid/view/View;)V
    invoke-virtual {p0, v0}, Lcom/privacyfblite/extension/SettingsActivity;->setContentView(Landroid/view/View;)V
    return-void
.end method

.method private addToggle(Landroid/widget/LinearLayout;Ljava/lang/String;Ljava/lang/String;Z)V
    .locals 4
    new-instance v0, Landroid/widget/CheckBox;
    invoke-direct {v0, p0}, Landroid/widget/CheckBox;-><init>(Landroid/content/Context;)V
    invoke-virtual {v0, p3}, Landroid/widget/CheckBox;->setText(Ljava/lang/CharSequence;)V
    const/4 v1, -0x1
    invoke-virtual {v0, v1}, Landroid/widget/CheckBox;->setTextColor(I)V
    invoke-static {p2, p4}, Lcom/privacyfblite/extension/Config;->get(Ljava/lang/String;Z)Z
    move-result v1
    invoke-virtual {v0, v1}, Landroid/widget/CheckBox;->setChecked(Z)V
    invoke-virtual {v0, p2}, Landroid/widget/CheckBox;->setTag(Ljava/lang/Object;)V
    new-instance v1, Lcom/privacyfblite/extension/SettingsActivity$2;
    invoke-direct {v1, p0}, Lcom/privacyfblite/extension/SettingsActivity$2;-><init>(Lcom/privacyfblite/extension/SettingsActivity;)V
    invoke-virtual {v0, v1}, Landroid/widget/CheckBox;->setOnCheckedChangeListener(Landroid/widget/CompoundButton$OnCheckedChangeListener;)V
    const/16 v1, 0x0
    const/16 v2, 0xc
    const/16 v3, 0x0
    const/16 p0, 0xc
    invoke-virtual {v0, v1, v2, v3, p0}, Landroid/widget/CheckBox;->setPadding(IIII)V
    invoke-virtual {p1, v0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V
    return-void
.end method
