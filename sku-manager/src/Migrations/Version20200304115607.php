<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20200304115607 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->abortIf('postgresql' !== $this->connection->getDatabasePlatform()->getName(), 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('ALTER TABLE image ALTER source_url TYPE VARCHAR(1024)');
        $this->addSql('ALTER TABLE image ALTER source_small_url TYPE VARCHAR(1024)');
        $this->addSql('ALTER TABLE image ALTER file_location TYPE VARCHAR(512)');
        $this->addSql('ALTER TABLE image ALTER file_location_small TYPE VARCHAR(512)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->abortIf('postgresql' !== $this->connection->getDatabasePlatform()->getName(), 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('CREATE SCHEMA public');
        $this->addSql('ALTER TABLE image ALTER source_url TYPE VARCHAR(255)');
        $this->addSql('ALTER TABLE image ALTER source_small_url TYPE VARCHAR(255)');
        $this->addSql('ALTER TABLE image ALTER file_location TYPE VARCHAR(1024)');
        $this->addSql('ALTER TABLE image ALTER file_location_small TYPE VARCHAR(1024)');
    }
}
