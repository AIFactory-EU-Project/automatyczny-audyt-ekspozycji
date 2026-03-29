<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20191216140405 extends AbstractMigration
{
    public function getDescription() : string
    {
        return '';
    }

    public function up(Schema $schema) : void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->abortIf($this->connection->getDatabasePlatform()->getName() !== 'postgresql', 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('CREATE SEQUENCE access_token_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE client_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE fos_user_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE refresh_token_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE shop_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE import_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE auth_code_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE report_photo_analysis_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE segment_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE failed_import_attempt_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE camera_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE file_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE photo_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE TABLE access_token (id INT NOT NULL, client_id INT NOT NULL, user_id INT DEFAULT NULL, token VARCHAR(255) NOT NULL, expires_at INT DEFAULT NULL, scope VARCHAR(255) DEFAULT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_B6A2DD685F37A13B ON access_token (token)');
        $this->addSql('CREATE INDEX IDX_B6A2DD6819EB6921 ON access_token (client_id)');
        $this->addSql('CREATE INDEX IDX_B6A2DD68A76ED395 ON access_token (user_id)');
        $this->addSql('CREATE TABLE client (id INT NOT NULL, random_id VARCHAR(255) NOT NULL, redirect_uris TEXT NOT NULL, secret VARCHAR(255) NOT NULL, allowed_grant_types TEXT NOT NULL, PRIMARY KEY(id))');
        $this->addSql('COMMENT ON COLUMN client.redirect_uris IS \'(DC2Type:array)\'');
        $this->addSql('COMMENT ON COLUMN client.allowed_grant_types IS \'(DC2Type:array)\'');
        $this->addSql('CREATE TABLE fos_user (id INT NOT NULL, username VARCHAR(180) NOT NULL, username_canonical VARCHAR(180) NOT NULL, email VARCHAR(180) NOT NULL, email_canonical VARCHAR(180) NOT NULL, enabled BOOLEAN NOT NULL, salt VARCHAR(255) DEFAULT NULL, password VARCHAR(255) NOT NULL, last_login TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, confirmation_token VARCHAR(180) DEFAULT NULL, password_requested_at TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, roles TEXT NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_957A647992FC23A8 ON fos_user (username_canonical)');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_957A6479A0D96FBF ON fos_user (email_canonical)');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_957A6479C05FB297 ON fos_user (confirmation_token)');
        $this->addSql('COMMENT ON COLUMN fos_user.roles IS \'(DC2Type:array)\'');
        $this->addSql('CREATE TABLE refresh_token (id INT NOT NULL, client_id INT NOT NULL, user_id INT DEFAULT NULL, token VARCHAR(255) NOT NULL, expires_at INT DEFAULT NULL, scope VARCHAR(255) DEFAULT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_C74F21955F37A13B ON refresh_token (token)');
        $this->addSql('CREATE INDEX IDX_C74F219519EB6921 ON refresh_token (client_id)');
        $this->addSql('CREATE INDEX IDX_C74F2195A76ED395 ON refresh_token (user_id)');
        $this->addSql('CREATE TABLE shop (id INT NOT NULL, name VARCHAR(255) NOT NULL, code VARCHAR(255) NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE TABLE import (id INT NOT NULL, date_time TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, is_complete BOOLEAN DEFAULT \'false\' NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE TABLE auth_code (id INT NOT NULL, client_id INT NOT NULL, user_id INT DEFAULT NULL, token VARCHAR(255) NOT NULL, redirect_uri TEXT NOT NULL, expires_at INT DEFAULT NULL, scope VARCHAR(255) DEFAULT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_5933D02C5F37A13B ON auth_code (token)');
        $this->addSql('CREATE INDEX IDX_5933D02C19EB6921 ON auth_code (client_id)');
        $this->addSql('CREATE INDEX IDX_5933D02CA76ED395 ON auth_code (user_id)');
        $this->addSql('CREATE TABLE report_photo_analysis (id INT NOT NULL, planogram_id INT DEFAULT NULL, photo_id INT DEFAULT NULL, date_time TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, data JSON NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_C38374C75AFB77AB ON report_photo_analysis (planogram_id)');
        $this->addSql('CREATE INDEX IDX_C38374C77E9E4C8C ON report_photo_analysis (photo_id)');
        $this->addSql('CREATE TABLE planogram_element (id SERIAL NOT NULL, planogram_id INT DEFAULT NULL, sku_id INT DEFAULT NULL, shelf INT NOT NULL, position INT NOT NULL, faces_count INT NOT NULL, stack_count INT NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_9F9F2D6D5AFB77AB ON planogram_element (planogram_id)');
        $this->addSql('CREATE INDEX IDX_9F9F2D6D1777D41C ON planogram_element (sku_id)');
        $this->addSql('CREATE TABLE shop_planogram_assignment (id SERIAL NOT NULL, segment_id INT DEFAULT NULL, shop_id INT DEFAULT NULL, planogram_id INT DEFAULT NULL, start_date_time TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, end_date_time TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_AAF32B45DB296AAD ON shop_planogram_assignment (segment_id)');
        $this->addSql('CREATE INDEX IDX_AAF32B454D16C4DD ON shop_planogram_assignment (shop_id)');
        $this->addSql('CREATE INDEX IDX_AAF32B455AFB77AB ON shop_planogram_assignment (planogram_id)');
        $this->addSql('CREATE TABLE segment (id INT NOT NULL, name VARCHAR(255) NOT NULL, type VARCHAR(255) CHECK(type IN (\'READY_MEAL\', \'QUICK_SNACK\', \'GRILL\')) NOT NULL, PRIMARY KEY(id))');
        $this->addSql('COMMENT ON COLUMN segment.type IS \'(DC2Type:SegmentType)\'');
        $this->addSql('CREATE TABLE failed_import_attempt (id INT NOT NULL, camera_id INT DEFAULT NULL, attempt_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_BAE35AE4B47685CD ON failed_import_attempt (camera_id)');
        $this->addSql('CREATE TABLE sku (id SERIAL NOT NULL, file_id INT DEFAULT NULL, name VARCHAR(255) NOT NULL, index VARCHAR(255) NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_F9038C493CB796C ON sku (file_id)');
        $this->addSql('CREATE TABLE camera (id INT NOT NULL, segment_id INT DEFAULT NULL, shop_id INT DEFAULT NULL, type VARCHAR(255) NOT NULL, ip VARCHAR(20) NOT NULL, manipulation_settings TEXT NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_3B1CEE05DB296AAD ON camera (segment_id)');
        $this->addSql('CREATE INDEX IDX_3B1CEE054D16C4DD ON camera (shop_id)');
        $this->addSql('CREATE TABLE planogram (id SERIAL NOT NULL, name VARCHAR(255) NOT NULL, description VARCHAR(255) NOT NULL, neural_network_id INT NOT NULL, version VARCHAR(255) NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE TABLE file (id INT NOT NULL, name VARCHAR(255) NOT NULL, directory TEXT NOT NULL, extension VARCHAR(10) DEFAULT NULL, storage_location VARCHAR(120) NOT NULL, temporary BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE TABLE photo (id INT NOT NULL, camera_id INT DEFAULT NULL, time TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, storage_id VARCHAR(255) NOT NULL, storage_type VARCHAR(255) CHECK(storage_type IN (\'LOCAL\', \'GOOGLE_CLOUD_STORAGE\')) NOT NULL, is_ai_processed BOOLEAN NOT NULL, is_manipulated BOOLEAN NOT NULL, is_valid BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_14B78418B47685CD ON photo (camera_id)');
        $this->addSql('COMMENT ON COLUMN photo.storage_type IS \'(DC2Type:FileStorageType)\'');
        $this->addSql('ALTER TABLE access_token ADD CONSTRAINT FK_B6A2DD6819EB6921 FOREIGN KEY (client_id) REFERENCES client (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE access_token ADD CONSTRAINT FK_B6A2DD68A76ED395 FOREIGN KEY (user_id) REFERENCES fos_user (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE refresh_token ADD CONSTRAINT FK_C74F219519EB6921 FOREIGN KEY (client_id) REFERENCES client (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE refresh_token ADD CONSTRAINT FK_C74F2195A76ED395 FOREIGN KEY (user_id) REFERENCES fos_user (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE auth_code ADD CONSTRAINT FK_5933D02C19EB6921 FOREIGN KEY (client_id) REFERENCES client (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE auth_code ADD CONSTRAINT FK_5933D02CA76ED395 FOREIGN KEY (user_id) REFERENCES fos_user (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE report_photo_analysis ADD CONSTRAINT FK_C38374C75AFB77AB FOREIGN KEY (planogram_id) REFERENCES planogram (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE report_photo_analysis ADD CONSTRAINT FK_C38374C77E9E4C8C FOREIGN KEY (photo_id) REFERENCES photo (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE planogram_element ADD CONSTRAINT FK_9F9F2D6D5AFB77AB FOREIGN KEY (planogram_id) REFERENCES planogram (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE planogram_element ADD CONSTRAINT FK_9F9F2D6D1777D41C FOREIGN KEY (sku_id) REFERENCES sku (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE shop_planogram_assignment ADD CONSTRAINT FK_AAF32B45DB296AAD FOREIGN KEY (segment_id) REFERENCES segment (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE shop_planogram_assignment ADD CONSTRAINT FK_AAF32B454D16C4DD FOREIGN KEY (shop_id) REFERENCES shop (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE shop_planogram_assignment ADD CONSTRAINT FK_AAF32B455AFB77AB FOREIGN KEY (planogram_id) REFERENCES planogram (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE failed_import_attempt ADD CONSTRAINT FK_BAE35AE4B47685CD FOREIGN KEY (camera_id) REFERENCES camera (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE sku ADD CONSTRAINT FK_F9038C493CB796C FOREIGN KEY (file_id) REFERENCES file (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE camera ADD CONSTRAINT FK_3B1CEE05DB296AAD FOREIGN KEY (segment_id) REFERENCES segment (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE camera ADD CONSTRAINT FK_3B1CEE054D16C4DD FOREIGN KEY (shop_id) REFERENCES shop (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE photo ADD CONSTRAINT FK_14B78418B47685CD FOREIGN KEY (camera_id) REFERENCES camera (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
    }

    public function down(Schema $schema) : void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->abortIf($this->connection->getDatabasePlatform()->getName() !== 'postgresql', 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('CREATE SCHEMA public');
        $this->addSql('ALTER TABLE access_token DROP CONSTRAINT FK_B6A2DD6819EB6921');
        $this->addSql('ALTER TABLE refresh_token DROP CONSTRAINT FK_C74F219519EB6921');
        $this->addSql('ALTER TABLE auth_code DROP CONSTRAINT FK_5933D02C19EB6921');
        $this->addSql('ALTER TABLE access_token DROP CONSTRAINT FK_B6A2DD68A76ED395');
        $this->addSql('ALTER TABLE refresh_token DROP CONSTRAINT FK_C74F2195A76ED395');
        $this->addSql('ALTER TABLE auth_code DROP CONSTRAINT FK_5933D02CA76ED395');
        $this->addSql('ALTER TABLE shop_planogram_assignment DROP CONSTRAINT FK_AAF32B454D16C4DD');
        $this->addSql('ALTER TABLE camera DROP CONSTRAINT FK_3B1CEE054D16C4DD');
        $this->addSql('ALTER TABLE shop_planogram_assignment DROP CONSTRAINT FK_AAF32B45DB296AAD');
        $this->addSql('ALTER TABLE camera DROP CONSTRAINT FK_3B1CEE05DB296AAD');
        $this->addSql('ALTER TABLE planogram_element DROP CONSTRAINT FK_9F9F2D6D1777D41C');
        $this->addSql('ALTER TABLE failed_import_attempt DROP CONSTRAINT FK_BAE35AE4B47685CD');
        $this->addSql('ALTER TABLE photo DROP CONSTRAINT FK_14B78418B47685CD');
        $this->addSql('ALTER TABLE report_photo_analysis DROP CONSTRAINT FK_C38374C75AFB77AB');
        $this->addSql('ALTER TABLE planogram_element DROP CONSTRAINT FK_9F9F2D6D5AFB77AB');
        $this->addSql('ALTER TABLE shop_planogram_assignment DROP CONSTRAINT FK_AAF32B455AFB77AB');
        $this->addSql('ALTER TABLE sku DROP CONSTRAINT FK_F9038C493CB796C');
        $this->addSql('ALTER TABLE report_photo_analysis DROP CONSTRAINT FK_C38374C77E9E4C8C');
        $this->addSql('DROP SEQUENCE access_token_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE client_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE fos_user_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE refresh_token_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE shop_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE import_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE auth_code_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE report_photo_analysis_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE segment_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE failed_import_attempt_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE camera_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE file_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE photo_id_seq CASCADE');
        $this->addSql('DROP TABLE access_token');
        $this->addSql('DROP TABLE client');
        $this->addSql('DROP TABLE fos_user');
        $this->addSql('DROP TABLE refresh_token');
        $this->addSql('DROP TABLE shop');
        $this->addSql('DROP TABLE import');
        $this->addSql('DROP TABLE auth_code');
        $this->addSql('DROP TABLE report_photo_analysis');
        $this->addSql('DROP TABLE planogram_element');
        $this->addSql('DROP TABLE shop_planogram_assignment');
        $this->addSql('DROP TABLE segment');
        $this->addSql('DROP TABLE failed_import_attempt');
        $this->addSql('DROP TABLE sku');
        $this->addSql('DROP TABLE camera');
        $this->addSql('DROP TABLE planogram');
        $this->addSql('DROP TABLE file');
        $this->addSql('DROP TABLE photo');
    }
}
