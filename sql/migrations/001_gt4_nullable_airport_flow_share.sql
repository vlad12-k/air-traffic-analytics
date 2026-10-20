/*
V2 schema correction.

airport_flow_share_pct is undefined when an airport has
zero current-period passengers. SQL NULL preserves that
analytical meaning rather than fabricating a zero share.
*/

ALTER TABLE bi.GT4_Airport_Destination_Country_Flow
ALTER COLUMN airport_flow_share_pct DECIMAL(19,8) NULL;
