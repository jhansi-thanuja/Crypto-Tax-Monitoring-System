import React from "react";
import { Card, Collapse, List, Typography } from "antd";
import { InfoCircleOutlined } from "@ant-design/icons";

const { Title, Paragraph } = Typography;
const { Panel } = Collapse;

const TaxInfo = () => {
  // ✅ List of Tax Tips
  const taxTips = [
    {
      title: "💡 Long-Term Holding",
      description:
        "Hold your crypto assets for more than 12 months to benefit from lower tax rates on long-term capital gains.",
    },
    {
      title: "📚 Maintain Transaction Records",
      description:
        "Keep detailed records of your crypto transactions, including dates, prices, and quantities.",
    },
    {
      title: "🔄 Use Tax-Loss Harvesting",
      description:
        "Offset your capital gains by selling crypto assets that are at a loss to reduce your tax liability.",
    },
    {
      title: "🏦 Consider Tax-Advantaged Accounts",
      description:
        "Explore investing in crypto through tax-advantaged accounts to potentially reduce taxes.",
    },
  ];

  return (
    <div>
      <Title level={2}>📚 Understanding Crypto Tax Calculations</Title>

      {/* ✅ Basic Tax Info */}
      <Card
        title="📊 How Crypto Tax is Calculated"
        bordered={false}
        style={{ marginBottom: 24 }}
      >
        <Paragraph>
          Crypto taxation typically follows capital gains rules. When you sell
          your crypto assets for a higher price than you bought them, you
          generate a **profit (capital gain)**, which is subject to taxation.
          Conversely, if you sell at a lower price, you incur a **loss
          (capital loss)**.
        </Paragraph>
        <Collapse accordion>
          <Panel header="📝 Example: Buy and Sell Scenario" key="1">
            <Paragraph>
              <strong>Buy:</strong> You purchase 1 Bitcoin at ₹30,00,000.  
              <br />
              <strong>Sell:</strong> You sell 1 Bitcoin at ₹35,00,000.  
              <br />
              <strong>Profit:</strong> ₹35,00,000 - ₹30,00,000 = ₹5,00,000  
              <br />
              <strong>Tax:</strong> If the tax rate is 15%, you’ll owe:  
              ₹5,00,000 × 0.15 = ₹75,000.
            </Paragraph>
          </Panel>

          <Panel header="📈 Short-Term vs Long-Term Gains" key="2">
            <Paragraph>
              - **Short-Term Gains:** Taxed as regular income if the holding
              period is less than 12 months.  
              - **Long-Term Gains:** Taxed at reduced rates if held for more
              than 12 months.
            </Paragraph>
          </Panel>

          <Panel header="🔄 Tax-Loss Harvesting" key="3">
            <Paragraph>
              Offset your capital gains by selling assets that are currently at
              a loss. This strategy helps reduce overall tax liability.
            </Paragraph>
          </Panel>
        </Collapse>
      </Card>

      {/* ✅ Tax Tips */}
      <Card
        title="💡 Tips to Optimize Your Crypto Taxes"
        bordered={false}
        style={{ marginBottom: 24 }}
      >
        <List
          itemLayout="horizontal"
          dataSource={taxTips}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={<InfoCircleOutlined style={{ fontSize: 20, color: "#1890ff" }} />}
                title={<strong>{item.title}</strong>}
                description={item.description}
              />
            </List.Item>
          )}
        />
      </Card>

      {/* ✅ Disclaimer */}
      <Card type="inner" style={{ backgroundColor: "#f5f5f5" }}>
        <Paragraph>
          ⚠️ <strong>Disclaimer:</strong> The information provided is for
          educational purposes only and should not be considered as financial or
          tax advice. Please consult with a professional tax advisor for
          personalized guidance.
        </Paragraph>
      </Card>
    </div>
  );
};

export default TaxInfo;
