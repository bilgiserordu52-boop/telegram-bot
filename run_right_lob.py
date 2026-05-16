from core.right_lob_gateway import gateway

print("🟠 RIGHT LOB TEST START")

print(gateway.handle_sync("ping"))
print(gateway.handle_sync("selam"))
print(gateway.handle_sync("/system"))

print(gateway.ui())

print("🟢 RIGHT LOB OK")
