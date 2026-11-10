.class Lcom/privacyfblite/extension/SettingsActivity$1;
.super Ljava/lang/Object;
.implements Landroid/view/View$OnClickListener;

.field final synthetic this$0:Lcom/privacyfblite/extension/SettingsActivity;

.method constructor <init>(Lcom/privacyfblite/extension/SettingsActivity;)V
    .locals 0
    iput-object p1, p0, Lcom/privacyfblite/extension/SettingsActivity$1;->this$0:Lcom/privacyfblite/extension/SettingsActivity;
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public onClick(Landroid/view/View;)V
    .locals 2
    iget-object v0, p0, Lcom/privacyfblite/extension/SettingsActivity$1;->this$0:Lcom/privacyfblite/extension/SettingsActivity;
    const-string v1, "Restarting…"
    const/4 p1, 0x0
    invoke-static {v0, v1, p1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
    move-result-object v1
    invoke-virtual {v1}, Landroid/widget/Toast;->show()V
    invoke-static {v0}, Lcom/privacyfblite/extension/RestartHelper;->restart(Landroid/content/Context;)V
    return-void
.end method
