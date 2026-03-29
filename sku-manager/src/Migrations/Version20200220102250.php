<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20200220102250 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->abortIf('postgresql' !== $this->connection->getDatabasePlatform()->getName(), 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('CREATE SEQUENCE log_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE image_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE training_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE product_group_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE brand_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE product_class_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE product_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE "user_id_seq" INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE SEQUENCE system_id_seq INCREMENT BY 1 MINVALUE 1 START 1');
        $this->addSql('CREATE TABLE log (id INT NOT NULL, message TEXT NOT NULL, context JSON NOT NULL, level SMALLINT NOT NULL, level_name VARCHAR(50) NOT NULL, extra JSON NOT NULL, created_at TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, system_id INT NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX system_id_idx ON log (system_id)');
        $this->addSql('CREATE TABLE image (id INT NOT NULL, product_id INT NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, source_url VARCHAR(255) NOT NULL, source_small_url VARCHAR(255) NOT NULL, tags VARCHAR(512) NOT NULL, additional_meta JSON NOT NULL, main BOOLEAN NOT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_C53D045F4584665A ON image (product_id)');
        $this->addSql('CREATE TABLE training (id INT NOT NULL, product_group_id INT NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, status INT NOT NULL, stale INT NOT NULL, hash VARCHAR(255) NOT NULL, data_snapshot JSON NOT NULL, start_date TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, scheduled_start_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, end_date TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, estimated_end_date TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, file_location VARCHAR(255) DEFAULT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_D5128A8F35E4B3D0 ON training (product_group_id)');
        $this->addSql('CREATE TABLE product_group (id INT NOT NULL, system_id INT NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, name VARCHAR(255) NOT NULL, description VARCHAR(512) NOT NULL, available_offline BOOLEAN NOT NULL, available_online BOOLEAN NOT NULL, tags VARCHAR(512) NOT NULL, additional_meta JSON NOT NULL, training_status INT NOT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_CC9C3F99D0952FA5 ON product_group (system_id)');
        $this->addSql('CREATE TABLE product_group_product (product_group_id INT NOT NULL, product_id INT NOT NULL, PRIMARY KEY(product_group_id, product_id))');
        $this->addSql('CREATE INDEX IDX_8FA74C5335E4B3D0 ON product_group_product (product_group_id)');
        $this->addSql('CREATE INDEX IDX_8FA74C534584665A ON product_group_product (product_id)');
        $this->addSql('CREATE TABLE brand (id INT NOT NULL, system_id INT NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, name VARCHAR(255) NOT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_1C52F958D0952FA5 ON brand (system_id)');
        $this->addSql('CREATE TABLE product_class (id INT NOT NULL, system_id INT NOT NULL, parent_class_id INT DEFAULT NULL, name VARCHAR(255) NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_4C1762C3D0952FA5 ON product_class (system_id)');
        $this->addSql('CREATE INDEX IDX_4C1762C375CDA7C1 ON product_class (parent_class_id)');
        $this->addSql('CREATE TABLE product (id INT NOT NULL, system_id INT NOT NULL, brand_id INT DEFAULT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, name VARCHAR(255) NOT NULL, tags VARCHAR(512) NOT NULL, additional_meta JSON NOT NULL, client_id VARCHAR(128) NOT NULL, player BOOLEAN NOT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE INDEX IDX_D34A04ADD0952FA5 ON product (system_id)');
        $this->addSql('CREATE INDEX IDX_D34A04AD44F5D008 ON product (brand_id)');
        $this->addSql('CREATE TABLE product_product_class (product_id INT NOT NULL, product_class_id INT NOT NULL, PRIMARY KEY(product_id, product_class_id))');
        $this->addSql('CREATE INDEX IDX_96FA7E314584665A ON product_product_class (product_id)');
        $this->addSql('CREATE INDEX IDX_96FA7E3121B06187 ON product_product_class (product_class_id)');
        $this->addSql('CREATE TABLE "user" (id INT NOT NULL, system_id INT NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, email VARCHAR(180) NOT NULL, roles JSON NOT NULL, password VARCHAR(255) NOT NULL, password_requested_at TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, confirmation_token VARCHAR(255) DEFAULT NULL, failed_attempts INT DEFAULT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_8D93D649E7927C74 ON "user" (email)');
        $this->addSql('CREATE INDEX IDX_8D93D649D0952FA5 ON "user" (system_id)');
        $this->addSql('CREATE TABLE system (id INT NOT NULL, created_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, updated_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, name VARCHAR(255) NOT NULL, terminate_date TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL, contact VARCHAR(255) NOT NULL, region VARCHAR(255) NOT NULL, active BOOLEAN NOT NULL, PRIMARY KEY(id))');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_C94D118B5E237E06 ON system (name)');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_C94D118BF62F176 ON system (region)');
        $this->addSql('ALTER TABLE image ADD CONSTRAINT FK_C53D045F4584665A FOREIGN KEY (product_id) REFERENCES product (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE training ADD CONSTRAINT FK_D5128A8F35E4B3D0 FOREIGN KEY (product_group_id) REFERENCES product_group (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_group ADD CONSTRAINT FK_CC9C3F99D0952FA5 FOREIGN KEY (system_id) REFERENCES system (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_group_product ADD CONSTRAINT FK_8FA74C5335E4B3D0 FOREIGN KEY (product_group_id) REFERENCES product_group (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_group_product ADD CONSTRAINT FK_8FA74C534584665A FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE brand ADD CONSTRAINT FK_1C52F958D0952FA5 FOREIGN KEY (system_id) REFERENCES system (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_class ADD CONSTRAINT FK_4C1762C3D0952FA5 FOREIGN KEY (system_id) REFERENCES system (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_class ADD CONSTRAINT FK_4C1762C375CDA7C1 FOREIGN KEY (parent_class_id) REFERENCES product_class (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product ADD CONSTRAINT FK_D34A04ADD0952FA5 FOREIGN KEY (system_id) REFERENCES system (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product ADD CONSTRAINT FK_D34A04AD44F5D008 FOREIGN KEY (brand_id) REFERENCES brand (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_product_class ADD CONSTRAINT FK_96FA7E314584665A FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE product_product_class ADD CONSTRAINT FK_96FA7E3121B06187 FOREIGN KEY (product_class_id) REFERENCES product_class (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('ALTER TABLE "user" ADD CONSTRAINT FK_8D93D649D0952FA5 FOREIGN KEY (system_id) REFERENCES system (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->abortIf('postgresql' !== $this->connection->getDatabasePlatform()->getName(), 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('CREATE SCHEMA public');
        $this->addSql('ALTER TABLE training DROP CONSTRAINT FK_D5128A8F35E4B3D0');
        $this->addSql('ALTER TABLE product_group_product DROP CONSTRAINT FK_8FA74C5335E4B3D0');
        $this->addSql('ALTER TABLE product DROP CONSTRAINT FK_D34A04AD44F5D008');
        $this->addSql('ALTER TABLE product_class DROP CONSTRAINT FK_4C1762C375CDA7C1');
        $this->addSql('ALTER TABLE product_product_class DROP CONSTRAINT FK_96FA7E3121B06187');
        $this->addSql('ALTER TABLE image DROP CONSTRAINT FK_C53D045F4584665A');
        $this->addSql('ALTER TABLE product_group_product DROP CONSTRAINT FK_8FA74C534584665A');
        $this->addSql('ALTER TABLE product_product_class DROP CONSTRAINT FK_96FA7E314584665A');
        $this->addSql('ALTER TABLE product_group DROP CONSTRAINT FK_CC9C3F99D0952FA5');
        $this->addSql('ALTER TABLE brand DROP CONSTRAINT FK_1C52F958D0952FA5');
        $this->addSql('ALTER TABLE product_class DROP CONSTRAINT FK_4C1762C3D0952FA5');
        $this->addSql('ALTER TABLE product DROP CONSTRAINT FK_D34A04ADD0952FA5');
        $this->addSql('ALTER TABLE "user" DROP CONSTRAINT FK_8D93D649D0952FA5');
        $this->addSql('DROP SEQUENCE log_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE image_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE training_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE product_group_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE brand_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE product_class_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE product_id_seq CASCADE');
        $this->addSql('DROP SEQUENCE "user_id_seq" CASCADE');
        $this->addSql('DROP SEQUENCE system_id_seq CASCADE');
        $this->addSql('DROP TABLE log');
        $this->addSql('DROP TABLE image');
        $this->addSql('DROP TABLE training');
        $this->addSql('DROP TABLE product_group');
        $this->addSql('DROP TABLE product_group_product');
        $this->addSql('DROP TABLE brand');
        $this->addSql('DROP TABLE product_class');
        $this->addSql('DROP TABLE product');
        $this->addSql('DROP TABLE product_product_class');
        $this->addSql('DROP TABLE "user"');
        $this->addSql('DROP TABLE system');
    }
}
