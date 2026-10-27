# Customer Segmentation Using RFM Analysis

## Project Overview
This project analyzes online retail transactions to understand customer purchasing behavior and group customers into meaningful segments using RFM analysis.

RFM stands for:
- **Recency:** How recently a customer purchased.
- **Frequency:** How many distinct purchases a customer made.
- **Monetary:** The total recorded value of a customer's purchases.

## Business Problem
Retail businesses need to identify valuable customers, understand customers who may need re-engagement, and develop more targeted marketing strategies.

## Tools and Technologies
- Python 3.11
- Pandas
- OpenPyXL
- Matplotlib
- VS Code

## Dataset
The project uses the UCI Online Retail dataset, which contains transaction records from a UK-based online retailer.

Dataset source: https://archive.ics.uci.edu/dataset/352/online+retail

## Project Workflow
1. Loaded the retail transaction dataset.
2. Checked the data structure and column names.
3. Removed records with missing required values, cancelled invoices, and invalid purchase quantities or prices.
4. Calculated transaction value using quantity multiplied by unit price.
5. Aggregated transaction data by customer.
6. Calculated Recency, Frequency, and Monetary metrics.
7. Assigned RFM scores and grouped customers into six segments.
8. Exported customer-level results and segment summaries.
9. Created charts showing customer counts and revenue by segment.

## Key Results
- Original transaction records: 541,909
- Cleaned transaction records: 397,884
- Unique customers analyzed: 4,338
- Customer segments created: 6

## Customer Segments
- Champions
- Loyal Customers
- Potential Loyalists
- At Risk
- Need Attention
- Regular Customers

## Key Findings
- Need Attention was the largest segment, with 1,074 customers (24.76%).
- Champions included 947 customers (21.83%).
- Champions generated approximately £5.76 million in recorded transaction value.
- The At Risk segment contained 661 customers (15.24%).

These results are based on the project's current RFM scoring rules. Segment labels are analytical classifications, not guaranteed predictions of future customer behavior.

## Output Files
- `output/customer_rfm_segments.csv` — customer-level RFM metrics, scores, and segments.
- `output/segment_summary.csv` — customer counts and spending summaries by segment.
- `output/customer_segments.png` — customer count chart.
- `output/revenue_by_segment.png` — revenue by segment.

## Business Recommendations
1. Develop loyalty and retention campaigns for Champions.
2. Test targeted re-engagement campaigns for At Risk customers.
3. Investigate the large Need Attention segment to understand customer inactivity and opportunities for renewed engagement.

## Limitations
- RFM scores use relative rankings within this dataset.
- Segment definitions are based on predefined rules.
- Revenue represents recorded transaction value, not profit.
- The analysis describes historical behavior and does not predict future purchases.

## Future Improvements
- Create an interactive dashboard using Power BI.
- Compare customer segments over different time periods.
- Test clustering methods such as K-means.
- Evaluate customer retention and repeat purchase behavior.

## Author
Deepika B