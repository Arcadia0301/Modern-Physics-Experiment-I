total = 0.0
m = 0.0
error = 0.0

with open("out.txt", "r") as f:
    for line in f:
        line = line.strip()
        # 跳过表头或分隔行
        if not line or line.startswith("===") or "organ ID" in line:
            continue
        # 用空格分列
        parts = line.split()
        if len(parts) >= 3:
            try:
                mass = float(parts[1])
                dose = float(parts[2])
                relerror = float(parts[3])
                total += mass * dose/1000
                m += mass/1000
                error += mass * dose * relerror/1000
            except ValueError:
                continue

print(total,m,error*3.7*10**10*25*10**-3*72.9857/((1.51*10**-4)**2)/3600)
