<?php

namespace App\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\PlanogramRepository")
 */
class Planogram
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue(strategy="IDENTITY")
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $name;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $description;

    /**
     * @ORM\Column(type="integer")
     */
    private $neuralNetworkId;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\ShopPlanogramAssignment", mappedBy="planogram")
     */
    private $shopPlanogramAssignments;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\PlanogramElement", mappedBy="planogram")
     */
    private $planogramElements;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\ReportPhotoAnalysis", mappedBy="planogram")
     */
    private $reportPhotoAnalyses;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $version;

    public function __construct()
    {
        $this->shopPlanogramAssignments = new ArrayCollection();
        $this->planogramElements = new ArrayCollection();
        $this->reportPhotoAnalyses = new ArrayCollection();
    }

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

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(string $description): self
    {
        $this->description = $description;

        return $this;
    }

    public function getNeuralNetworkId(): ?int
    {
        return $this->neuralNetworkId;
    }

    public function setNeuralNetworkId(int $neuralNetworkId): self
    {
        $this->neuralNetworkId = $neuralNetworkId;

        return $this;
    }

    public function getShopPlanogramAssignments(): Collection
    {
        return $this->shopPlanogramAssignments;
    }

    public function getPlanogramElements(): Collection
    {
        return $this->planogramElements;
    }

    public function getReportPhotoAnalyses(): Collection
    {
        return $this->reportPhotoAnalyses;
    }

    public function getVersion(): string
    {
        return $this->version;
    }

    public function setVersion(string $version): self
    {
        $this->version = $version;

        return $this;
    }
}
