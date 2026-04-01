-- ══════════════════════════════════════════════════════════════════════════
-- MEGA-STACK v2.5 — MSSQL Initial Setup Script
-- Hedef: İlk sistem kullanıcıları ve v2.5 DB yetkileri
-- Çalıştırılma: docker exec mssql /opt/mssql-tools18/bin/sqlcmd ...
-- ══════════════════════════════════════════════════════════════════════════

-- v2.5 sistem veritabanını oluştur
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'MegaStackDB')
BEGIN
    CREATE DATABASE MegaStackDB;
    PRINT 'MegaStackDB oluşturuldu.';
END
GO

USE MegaStackDB;
GO

-- Sistem meta tablosu
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='system_info' AND xtype='U')
BEGIN
    CREATE TABLE system_info (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        [key]       NVARCHAR(128) NOT NULL UNIQUE,
        [value]     NVARCHAR(MAX),
        created_at  DATETIME2 DEFAULT GETUTCDATE(),
        updated_at  DATETIME2 DEFAULT GETUTCDATE()
    );

    INSERT INTO system_info ([key], [value])
    VALUES ('schema_version', '2.5.0'),
           ('installed_at', CONVERT(NVARCHAR(50), GETUTCDATE(), 127));

    PRINT 'system_info tablosu oluşturuldu.';
END
GO

-- Uygulama servisleri için read-only login (opsiyonel)
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = N'megastack_reader')
BEGIN
    CREATE LOGIN megastack_reader WITH PASSWORD = N'$(READER_PASSWORD)', CHECK_POLICY = OFF;
    PRINT 'megastack_reader login oluşturuldu.';
END
GO

USE MegaStackDB;
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'megastack_reader')
BEGIN
    CREATE USER megastack_reader FOR LOGIN megastack_reader;
    ALTER ROLE db_datareader ADD MEMBER megastack_reader;
    PRINT 'megastack_reader user oluşturuldu ve db_datareader yetkisi verildi.';
END
GO

PRINT '═══ MEGA-STACK v2.5 MSSQL Setup tamamlandı ═══';
GO
