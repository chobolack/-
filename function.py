import math

# 求sin值
def sin(angle):
    value_sin = math.sin(math.radians(angle))
    return value_sin

# 求cos值
def cos(angle):
    value_cos = math.cos(math.radians(angle))
    return value_cos

# 求兩邊夾角角度
def Cos(adjacent, hypotenuse):
    degree = math.degrees(math.acos(adjacent / hypotenuse))
    return degree

# 三邊求角度
def cosine(side_A, side_B, side_C):
    degree_C = math.degrees(math.acos((side_A**2 + side_B**2 - side_C**2) / (2 * side_A * side_B)))
    return degree_C

# 兩邊一角求第三邊
def Cosine(side_A, side_B, angle_C):
    side_C = math.sqrt(side_A**2 + side_B**2 - (2 * side_A * side_B * cos(angle_C)))
    return side_C

#===================================================以上為自訂三角函數===================================================

debug_before = {}
debug_after = {}

# 抬升前力分析
def Before(Line_OA, Line_AB, Line_BC, Line_CO, Line_CD, Line_CE, Mass, Gravity):

    Line_AC = math.sqrt(Line_OA**2 + Line_CO**2)

    angle_A = Cos(Line_OA, Line_AC) + cosine(Line_AB, Line_AC, Line_BC)
    angle_B = cosine(Line_AB, Line_BC, Line_AC)
    angle_C = Cos(Line_CO, Line_AC) + cosine(Line_BC, Line_AC, Line_AB)
    
    # 油壓桿長度
    Line_DE = Cosine(Line_CD, Line_CE, angle_C)
    
    angle_D = cosine(Line_CD, Line_DE, Line_CE)

    # 三點力
    Force_AB = (Mass * Gravity) / sin(angle_A)
    Force_DE = (Force_AB * sin(180 - angle_B) * Line_BC) / (cos(90 - angle_D) * Line_CD)
    Force_C = Cosine(Force_AB, Force_DE, angle_B-angle_D)

    # 檢測用
    debug_before['\u2220A'] = angle_A
    debug_before['\u2220B'] = angle_B
    debug_before['\u2220C'] = angle_C
    debug_before['\u2220D'] = angle_D
    debug_before['油壓桿長度'] = Line_DE

    return Force_AB, Force_DE, Force_C

# 抬升後力分析
def After(Line_OA, Line_AB, Line_BC, Line_CO, Line_CD, Line_CE, Mass, Gravity):

    Line_CO = Line_CO - 2000
    Line_AC = math.sqrt(Line_OA**2 + Line_CO**2)

    angle_A = Cos(Line_OA, Line_AC) + cosine(Line_AB, Line_AC, Line_BC)
    angle_B = cosine(Line_AB, Line_BC, Line_AC)
    angle_C = Cos(Line_CO, Line_AC) + cosine(Line_BC, Line_AC, Line_AB)
    
    # 油壓桿長度
    Line_DE = Cosine(Line_CD, Line_CE, angle_C)
    
    angle_D = cosine(Line_CD, Line_DE, Line_CE)

    # 三點力
    Force_AB = (Mass * Gravity) / sin(angle_A)
    Force_DE = (Force_AB * sin(180 - angle_B) * Line_BC) / (cos(90 - angle_D) * Line_CD)
    Force_C = Cosine(Force_AB, Force_DE, angle_B-angle_D)

    # 補正角
    θ = math.degrees(math.acos((Force_DE * cos(angle_D) - Force_AB * cos(angle_B)) / Force_C))

    # 剪力圖
    Ra = -Force_AB * sin(angle_B)
    Rb = Force_C * sin(θ)
    Aa = Ra * ((Line_BC - Line_CD) / 1000) 
    Ab = Rb * (Line_CD / 1000)
    bool = False
    if round(-Aa, 3) == round(Ab, 3):
        bool = True

    # 彎矩圖
    Mmax = Aa 

    # 檢測用
    debug_after['\u2220A'] = angle_A
    debug_after['\u2220B'] = angle_B
    debug_after['\u2220C'] = angle_C
    debug_after['\u2220D'] = angle_D
    debug_after['油壓桿長度'] = Line_DE
    debug_after['剪力圖D點左側面積'] = Aa
    debug_after['剪力圖D點右側面積'] = Ab

    return Force_AB, Force_DE, Force_C, θ, Ra, Rb, bool, Mmax, angle_D

# 鋼管
def Pipe(a, b, c):
    A = a*b - ((a-(2*c)) *( b-(2*c)))
    I = 1/12 * (b/1000) * (a/1000)**3 - 1/12 * ((b-(2*c))/1000) * ((a-(2*c))/1000)**3
    return A, I

#上拉桿最大應力點
def abc(Mmax, y, I, Force_DE, angle_D, A):
    sigma_Max = (-Mmax * (y/1000) / I) / (10**6)
    sigma = (Force_DE * cos(angle_D) / A)
    sigma_toatl = (sigma_Max + sigma)
    return sigma_Max, sigma, sigma_toatl

# 安全係數
def SafetyFactor(a, b, c, d):
    sf = (a * (10**6) * b * 2) / ((c/1000) * d)
    return sf

# 銷
def Pin(Fab, W, Syt):
    d = (1.5*(4 * Fab * W) / (math.pi * (Syt / 2))) ** (1 / 3)
    return d

def welding(Pa, Ptr, h, A, I):
    
    return 

# 檢測用
def check_debug_before(num):
    print("抬升前的其他數據")
    for key, value in debug_before.items():
        print(f"{key}: {round(value, num)}")

def check_debug_after(num):
    print("抬升後的其他數據")
    for key, value in debug_after.items():
        print(f"{key}: {round(value, num)}")