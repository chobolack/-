import function
import matplotlib.pyplot as plt

#===================================================以下為輸出設定===================================================

# 取小數後幾位
num = 2

# 顯示顏色
green = "\033[92m"
red = "\033[91m"

# 句尾重置顏色
color_end = "\033[0m"

# 標註
check_mark = "\u2713"
failed_mark = "\u2717"

#===================================================以下為參數設定===================================================

# 車重
Mass = 1000     
Gravity = 9.81

# 機械車位參數
Line_OA = 2508
Line_AB = 2000
Line_CO = 3000
Line_BC = 2700
Line_DC = 1350
Line_CE = 2000

# 鋼管參數
Pipe_width = 100
Pipe_height = 150
Pipe_thickness = 5

# 鋼管材質的降伏強度
Syt_Pipe = 490

# 銷材質的降伏強度
Syt_Pin = 765

# 接頭寬
Clevis_width = 81

# 焊接材料的抗拉強度
Sut_welding = 638
#===================================================以下為函式呼叫===================================================

# 抬升前
before = function.Before(Line_OA, Line_AB, Line_BC, Line_CO, Line_DC, Line_CE, Mass, Gravity)
# 抬升後
after = function.After(Line_OA, Line_AB, Line_BC, Line_CO, Line_DC, Line_CE, Mass, Gravity)
# 拉桿的面積和I
pipe = function.Pipe(Pipe_height, Pipe_width, Pipe_thickness)
# 拉桿安全係數
Sf = function.SafetyFactor(Syt_Pipe, pipe[1], after[5], Pipe_height)
# 上拉桿最大應力點
MaxPoint = function.MaxPoint(after[7], Pipe_width, pipe[1], after[1], after[8], pipe[0])
# 銷直徑最小值
Pin = function.Pin(after[0], Clevis_width, Syt_Pin)
# 上焊接
Tau_Up = function.Tau_Up(after[0], after[9], Pipe_height, Pipe_width, Pipe_height, Pipe_thickness, Sut_welding)
# 下焊接
Tau_Down = function.Tau_Down(after[0], Pipe_height, Pipe_width, Pipe_height, Pipe_thickness, Sut_welding)

#===================================================以下為數據輸出===================================================

print("    負載分析(抬升前):")
print("")
print("    下拉桿")
print(f"    F (AB) = {round(before[0], num)} N")
print("")
print("    油壓桿")
print(f"    F (DE) = {round(before[1], num)} N")
print("")
print(f"    F (C) = {round(before[2], num)} N")

print("--------------------------------------------")

print("    負載分析(抬升後):")
print("")
print("    下拉桿")
print(f"    F (A'B') = {round(after[0],num)} N")
print("")
print("    油壓桿")
print(f"    F (D'E') = {round(after[1], num)} N")
print("")
print(f"    F (C') = {round(after[2], num)} N")

print("--------------------------------------------")

print("    應力分析:")
print("")
print("    上拉桿與Fc的夾角")
print("    \033[93m" + f"\u03B8 = {round(after[3], num)}\u00b0" + "\033[0m")
print("")
print("    剪力圖")
print(f"    B to D : {round(after[4], num)} N * {round((Line_BC - Line_DC)/1000, num)} m")   
print(f"    D to C : {round(after[5], num)} N * {round(Line_DC/1000, num)} m")
# 判斷剪力圖兩邊面積是否相等
if after[6] == True:
    print(f"    {green}result pass {check_mark}{color_end}")
else:
    print(f"    {red}result failed {failed_mark}{color_end}")
print("")
print("    彎矩圖")
print(f"    Mmax = {round(after[7], num)} Nm")

print("--------------------------------------------")

print("    鋼管分析:")
print("")
number = pipe[1]
formatted_number = "{:.4g}".format(number)
I = "{:.3f} * 10^{}".format(float(formatted_number.split('e')[0]), int(formatted_number.split('e')[1]))
print(f"    I = {I}")
print("")
print(f"    安全係數: {round(Sf, num)}")
# 判斷安全係數是否大於2
if Sf >= 2:
    print(f"    {green}result pass {check_mark}{color_end}")
else:
    print(f"    {red}result failed {failed_mark}{color_end}")
print("")
print("")
print("    上拉桿最大應力點:")
print("")
print("    Bending:")
print(f"    σmax = {round(MaxPoint[0], num)} MPa")
print("")
print("    Axial load:")
print(f"    σ = {round(MaxPoint[1], num)} MPa")
print("")
print(f"    σ = σmax + σ = {round(MaxPoint[2], num)} MPa")
print("")
print(f"    σallow = {Syt_Pipe / 2} MPa")
if (Syt_Pipe / 2) > MaxPoint[2]:
    print("    σallow > σ")
    print(f"    {green}result pass {check_mark}{color_end}")
else:
    print("    σallow < σ")
    print(f"    {red}result failed {failed_mark}{color_end}")

print("--------------------------------------------")

print("    銷分析:")
print("")
print(f"    Pin的最小直徑 d = {round(Pin, num)} mm")

print("--------------------------------------------")

print("    焊接分析:")
print("")
print(f"    τallow = {round(Tau_Up[2], num)} MPa")
print("")
print("    上拉桿焊接:")
print(f"    τ = {round(Tau_Up[0], num)} MPa")
if Tau_Up[1] == True:
    print("    τallow > τ")
    print(f"    {green}result pass {check_mark}{color_end}")
else:
    print("    τallow < τ")
    print(f"    {red}result failed {failed_mark}{color_end}")
print("")
print("    下拉桿焊接:")
print(f"    τ = {round(Tau_Down[0], num)} MPa")
if Tau_Down[1] == True:
    print("    τallow > τ")
    print(f"    {green}result pass {check_mark}{color_end}")
else:
    print("    τallow < τ")
    print(f"    {red}result failed {failed_mark}{color_end}")

print("--------------------------------------------")
# ===================================================以下為檢測數據===================================================

function.check_debug_before(num)
print("")
function.check_debug_after(num)
print("")
function.check_debug_Up(9)
print("")
function.check_debug_Down(9)

# ===================================================以下為剪力繪圖===================================================

Line_BD = Line_BC - Line_DC

# 剪力數據
shear_forces = [after[4], after[4], after[5], after[5]]
shear_positions = [0, Line_BD, Line_BD, Line_BC]

# 創建剪力圖
plt.figure(figsize=(10, 6))

# 繪製剪力圖
plt.subplot(2, 1, 1)
plt.step(shear_positions, shear_forces, where='post', color='red')
plt.title('Shear Force Diagram')
plt.xlabel('Position')
plt.ylabel('Shear Force')
plt.grid(True)

# 剪力圖設置
plt.xticks([0, Line_BD, Line_BC])
plt.yticks(shear_forces)
plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)
plt.xlim(0, Line_BC)
#plt.ylim(-max(abs(min(moments)), abs(max(moments))), max(abs(min(moments)), abs(max(moments))))

# 面積
plt.fill_between(shear_positions, shear_forces, color='skyblue', alpha=0.3) 

# ===================================================以下為彎矩繪圖===================================================

# 彎矩數據
moments = [0, after[7], 0]
positions2 = [0, Line_BD, Line_BC]

# 創建彎矩圖
plt.subplot(2, 1, 2)
plt.plot(positions2, moments, marker='o', linestyle='-', color='blue')
plt.title('Bending Moment Diagram')
plt.xlabel('Position')
plt.ylabel('Bending Moment')
plt.grid(True)

# 彎矩圖設置
plt.xticks([0, Line_BD, Line_BC])
plt.yticks(moments)
plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlim(0, Line_BC)
plt.ylim(-max(abs(min(moments)), abs(max(moments))), max(abs(min(moments)), abs(max(moments))))

# 面積
plt.fill_between(positions2, moments, color='skyblue', alpha=0.3)

plt.tight_layout()
plt.show()
