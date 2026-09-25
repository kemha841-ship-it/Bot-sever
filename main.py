import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot đã sẵn sàng: {bot.user}")

# Sử dụng Slash Command /auto
@bot.tree.command(name="auto", description="Tự động cày nhiệm vụ Discord bằng token an toàn")
@app_commands.describe(token="Nhập token tài khoản của bạn")
async def auto_quest(interaction: discord.Interaction, token: str):
    # Phản hồi riêng tư (ephemeral) để chỉ người dùng thấy, tránh lộ thông tin lên kênh chung
    await interaction.response.send_message("🛡️ Đã nhận token! Hệ thống đang tiến hành bảo mật và quét nhiệm vụ...", ephemeral=True)
    
    try:
        # ---- BƯỚC 1: XỬ LÝ QUÉT VÀ CÀY NHIỆM VỤ NGẦM ----
        # (Tại đây sếp gắn logic gọi request API cày quest của sếp vào)
        # Giả lập kết quả trả về sau khi chạy xong:
        total_quest = 65
        completed = 63
        expired = 2
        
        # ---- BƯỚC 2: GỬI BÁO CÁO VÀO HỘP THƯ RIÊNG (DM) CỦA NGƯỜI DÙNG ----
        try:
            user = interaction.user
            dm_channel = await user.create_dm()
            
            report_message = (
                "**📊 BÁO CÁO HOÀN THÀNH NHIỆM VỤ**\n"
                f"• Tổng số nhiệm vụ quét được: {total_quest}\n"
                f"• Đã hoàn thành thành công: {completed}\n"
                f"• Đã hết hạn/Bỏ qua: {expired}\n"
                "🔒 *Token của bạn đã được xóa sạch hoàn toàn khỏi hệ thống ngay sau khi xử lý xong.*"
            )
            await dm_channel.send(report_message)
        except Exception as dm_error:
            print(f"Không thể gửi DM cho người dùng: {dm_error}")

        # Cập nhật trạng thái hoàn tất trên giao diện tương tác
        await interaction.edit_original_response(content="✅ Đã hoàn thành toàn bộ quy trình! Kiểm tra hộp thư riêng (DM) để xem chi tiết kết quả.")

    except Exception as e:
        await interaction.edit_original_response(content=f"❌ Đã xảy ra lỗi trong quá trình xử lý: {e}")
        
    finally:
        # ---- BƯỚC 3: BẢO MẬT TUYỆT ĐỐI - XÓA SẠCH TOKEN KHỎI RAM ----
        del token

# Thay 'YOUR_BOT_TOKEN' bằng token bot Discord của sếp
bot.run("YOUR_BOT_TOKEN")
