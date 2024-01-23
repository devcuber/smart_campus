CREATE TABLE [device_type] (
  [id] INT PRIMARY KEY IDENTITY(1,1),
  [description] nvarchar(255),
  [created_at] datetime,
  [updated_at] datetime,
  [created_by] integer,
  [updated_by] integer
)
GO

CREATE TABLE [location_type] (
  [id] INT PRIMARY KEY IDENTITY(1,1),
  [description] nvarchar(255),
  [created_at] datetime,
  [updated_at] datetime,
  [created_by] integer,
  [updated_by] integer
)
GO

CREATE TABLE [location] (
  [id] INT PRIMARY KEY IDENTITY(1,1),
  [location_type_id] integer,
  [description] nvarchar(255),
  [location_id] integer,
  [created_at] datetime,
  [updated_at] datetime,
  [created_by] integer,
  [updated_by] integer
)
GO

CREATE TABLE [devices] (
  [id] varchar(50) PRIMARY KEY,
  [description] nvarchar(255),
  [device_type_id] integer,
  [location_id] integer,
  [active] integer,
  [created_at] datetime,
  [updated_at] datetime,
  [created_by] integer,
  [updated_by] integer
)
GO

CREATE TABLE [logs] (
  [id] INT PRIMARY KEY IDENTITY(1,1),
  [device_id] varchar(50),
  [created_at] datetime,
  [updated_at] datetime,
  [created_by] integer,
  [updated_by] integer,
  [code] nvarchar(255),
  [value] nvarchar(255)
)
GO

ALTER TABLE [devices] ADD FOREIGN KEY ([device_type_id]) REFERENCES [device_type] ([id])
GO

ALTER TABLE [devices] ADD FOREIGN KEY ([location_id]) REFERENCES [location] ([id])
GO

ALTER TABLE [location] ADD FOREIGN KEY ([location_id]) REFERENCES [location] ([id])
GO

ALTER TABLE [location] ADD FOREIGN KEY ([location_type_id]) REFERENCES [location_type] ([id])
GO

ALTER TABLE [logs] ADD FOREIGN KEY ([device_id]) REFERENCES [devices] ([id])
GO

CREATE VIEW presence_logs AS
select 
		tbl.id,
		tbl.device_id,
		tbl.code, 
		tbl.value,
		tbl.start_date,
		tbl.end_date,
		DATEDIFF(MINUTE, tbl.start_date, tbl.end_date) AS minutes
from (
	select 
		tbl.*,
		LAG(end_date) OVER (ORDER BY ID) AS start_date
	from (
		select l.* , 
			   LEAD(l.value) OVER (ORDER BY l.ID) AS NextValue,
			   LEAD(l.created_at) OVER (ORDER BY l.ID) AS end_date
		from devices as d
		inner join device_type as dt on d.device_type_id = dt.id and dt.id = 1 --device_type 1 presence sensor
		inner join logs		   as l  on l.device_id      =  d.id and code  = 'presence_state'
	) as tbl
	where value != NextValue
) tbl
GO