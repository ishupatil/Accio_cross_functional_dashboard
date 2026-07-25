
import matplotlib.pyplot as plt

regions = [
    "Maharashtra","Karnataka","Tamil Nadu","Delhi NCR",
    "Gujarat","West Bengal","Uttar Pradesh","Rajasthan"
]

revenue = [1875,1620,1480,1325,1180,1050,980,860]

plt.figure(figsize=(12,6))
plt.barh(regions, revenue)

plt.title("Revenue by Region")
plt.xlabel("Revenue (₹)")
plt.ylabel("Region")

plt.tight_layout()
plt.savefig("revenue_by_region.png", dpi=300)
plt.show()
