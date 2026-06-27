-- ============================================================
-- Azure SQL Warehouse — DDL for Food Delivery Analytics
-- ============================================================

-- 1. Fact Table: All orders
CREATE TABLE OrdersFact (
    OrderID               VARCHAR(20)   PRIMARY KEY,
    RestaurantID          VARCHAR(10)   NOT NULL,
    DriverID              VARCHAR(10)   NOT NULL,
    OrderTime             DATETIME      NOT NULL,
    FoodReadyTime         DATETIME      NOT NULL,
    DriverArrivalTime     DATETIME      NOT NULL,
    PickupTime            DATETIME      NOT NULL,
    DeliveryTime          DATETIME      NULL,
    PreparationDelayMins  DECIMAL(6,1)  NOT NULL,
    DriverWaitMins        DECIMAL(6,1)  NOT NULL,
    DeliveryDurationMins  DECIMAL(6,1)  NULL,
    OrderAmount           DECIMAL(10,2) NOT NULL,
    PaymentMethod         VARCHAR(30)   NOT NULL,
    OrderStatus           VARCHAR(20)   NOT NULL
);

-- 2. Summary Table: Restaurant performance metrics
CREATE TABLE RestaurantPerformance (
    RestaurantID          VARCHAR(10)   PRIMARY KEY,
    RestaurantName        VARCHAR(100)  NOT NULL,
    Cuisine               VARCHAR(50)   NOT NULL,
    Rating                DECIMAL(2,1)  NOT NULL,
    TotalOrders           INT           NOT NULL,
    AvgPreparationDelay   DECIMAL(6,2)  NOT NULL,
    AvgDriverWait         DECIMAL(6,2)  NOT NULL,
    AvgOrderAmount        DECIMAL(10,2) NOT NULL,
    TotalRevenue          DECIMAL(14,2) NOT NULL,
    DeliverySuccessRate   DECIMAL(5,2)  NOT NULL
);

-- 3. Summary Table: Review sentiment per restaurant
CREATE TABLE ReviewsSentiment (
    RestaurantID          VARCHAR(10)   PRIMARY KEY,
    RestaurantName        VARCHAR(100)  NOT NULL,
    TotalReviews          INT           NOT NULL,
    PositiveCount         INT           NOT NULL,
    NeutralCount          INT           NOT NULL,
    NegativeCount         INT           NOT NULL,
    PositiveReviewPct     DECIMAL(5,2)  NOT NULL,
    NegativeReviewPct     DECIMAL(5,2)  NOT NULL
);
