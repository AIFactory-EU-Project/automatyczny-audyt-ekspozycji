<?php

namespace App\Entity;

use ApiPlatform\Core\Annotation\ApiResource;
use DateTime;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\PhotoRepository")
 * @ApiResource()
 */
class Photo
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="datetime", options={"default": "CURRENT_TIMESTAMP"})
     */
    private $time;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $storageId;

    /**
     * @ORM\Column(type="FileStorageType")
     */
    private $storageType;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Camera", inversedBy="photos")
     * @ORM\JoinColumn(name="camera_id", referencedColumnName="id")
     */
    private $camera;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\Sku", mappedBy="photo")
     */
    private $skus;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\ReportPhotoAnalysis", mappedBy="planogram")
     */
    private $reportPhotoAnalyses;

    /**
     * @ORM\Column(type="boolean")
     */
    private $isAiProcessed;

    /**
     * @ORM\Column(type="boolean")
     */
    private $isManipulated;

    /**
     * @ORM\Column(type="boolean")
     */
    private $isValid;

    public function __construct()
    {
        $this->skus = new ArrayCollection();
        $this->reportPhotoAnalyses = new ArrayCollection();
        $this->time = new DateTime();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getTime(): ?\DateTimeInterface
    {
        return $this->time;
    }

    public function setTime(\DateTimeInterface $time): self
    {
        $this->time = $time;

        return $this;
    }

    public function getStorageId(): ?string
    {
        return $this->storageId;
    }

    public function setStorageId(string $storageId): self
    {
        $this->storageId = (string) $storageId;

        return $this;
    }

    public function getStorageType(): ?string
    {
        return $this->storageType;
    }

    public function setStorageType(string $storageType): self
    {
        $this->storageType = $storageType;

        return $this;
    }

    public function getCamera(): ?Camera
    {
        return $this->camera;
    }

    public function setCamera(Camera $camera): self
    {
        $this->camera = $camera;

        return $this;
    }

    public function getSkus(): Collection
    {
        return $this->skus;
    }

    public function getReportPhotoAnalyses(): Collection
    {
        return $this->reportPhotoAnalyses;
    }

    public function getIsAiProcessed(): ?bool
    {
        return $this->isAiProcessed;
    }

    public function setIsAiProcessed(bool $isAiProcessed): self
    {
        $this->isAiProcessed = $isAiProcessed;

        return $this;
    }

    public function getIsManipulated(): ?bool
    {
        return $this->isManipulated;
    }

    public function setIsManipulated(bool $isManipulated): self
    {
        $this->isManipulated = $isManipulated;

        return $this;
    }

    public function getIsValid(): ?bool
    {
        return $this->isValid;
    }

    public function setIsValid(bool $isValid): self
    {
        $this->isValid = $isValid;

        return $this;
    }
}
