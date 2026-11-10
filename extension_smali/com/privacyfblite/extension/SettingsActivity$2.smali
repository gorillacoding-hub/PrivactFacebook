.class Lcom/privacyfblite/extension/SettingsActivity$2;
.super Ljava/lang/Object;
.implements Landroid/widget/CompoundButton$OnCheckedChangeListener;

.field final synthetic this$0:Lcom/privacyfblite/extension/SettingsActivity;

.method constructor <init>(Lcom/privacyfblite/extension/SettingsActivity;)V
    .locals 0
    iput-object p1, p0, Lcom/privacyfblite/extension/SettingsActivity$2;->this$0:Lcom/privacyfblite/extension/SettingsActivity;
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public onCheckedChanged(Landroid/widget/CompoundButton;Z)V
    .locals 2
    invoke-virtual {p1}, Landroid/widget/CompoundButton;->getTag()Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Ljava/lang/String;
    if-nez v0, :done
    invoke-static {v0, p2}, Lcom/privacyfblite/extension/Config;->set(Ljava/lang/String;Z)V
    :done
    return-void
.end method
