<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\FileRepository")
 */
class File
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $name;

    /**
     * @ORM\Column(type="text")
     */
    private $directory;

    /**
     * @ORM\Column(type="string", length=10, nullable=true)
     */
    private $extension;

    /**
     * @ORM\Column(type="string", length=120)
     */
    private $storageLocation;

    /**
     * @ORM\Column(type="boolean")
     */
    private $temporary = false;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getDirectory(): ?string
    {
        return $this->directory;
    }

    public function setDirectory(string $directory): self
    {
        $this->directory = $directory;

        return $this;
    }

    public function getExtension(): ?string
    {
        return $this->extension;
    }

    public function setExtension(string $extension): self
    {
        $this->extension = $extension;

        return $this;
    }

    public function getFullPath(): string
    {
        return $this->getStorageLocation() . $this->getDirectory() . $this->getName();
    }

    public function getStorageLocation(): ?string
    {
        return $this->storageLocation;
    }

    public function setStorageLocation(string $storageLocation): self
    {
        $this->storageLocation = $storageLocation;

        return $this;
    }

    public function isTemporary(): bool
    {
        return $this->temporary;
    }

    public function setTemporary($isTemporary): self
    {
        $this->temporary = $isTemporary;

        return $this;
    }
}
